package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"

	_ "github.com/lib/pq"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func main() {
	// Create a new MCP server
	s := server.NewMCPServer(
		"BestForBuy",
		"1.0.0",
		server.WithResourceCapabilities(true, true),
		server.WithLogging(),
		server.WithRecovery(),
	)

	searchProducts := mcp.NewTool("search_products",
		mcp.WithDescription("Search from available products"),
		mcp.WithString("product_type",
			mcp.Required(),
			mcp.Description("Type of product you are looking for"),
			mcp.Enum("mobile", "laptop", "tablet"),
		),
		mcp.WithNumber("min_price",
			mcp.Required(),
			mcp.Description("Minimum price of product"),
		),
		mcp.WithNumber("max_price",
			mcp.Required(),
			mcp.Description("Maximum price of product"),
		),
		mcp.WithNumber("limit",
			mcp.Description("Max number of products should be returned"),
		),
	)

	s.AddTool(searchProducts, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		productType := request.Params.Arguments["product_type"].(string)
		minPrice := request.Params.Arguments["min_price"].(float64)
		maxPrice := request.Params.Arguments["max_price"].(float64)
		var limit *int64
		if val, ok := request.Params.Arguments["limit"].(int64); ok {
			limitVal := int64(val)
			limit = &limitVal
		}

		connStr := "host=localhost port=5432 user=postgres password=postgres dbname=products sslmode=disable"
		db, err := sql.Open("postgres", connStr)
		if err != nil {
			panic(err)
		}
		defer db.Close()

		products, err := fetchProducts(db, productType, minPrice, maxPrice, limit)

		r, err := json.Marshal(products)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal response: %w", err)
		}

		return mcp.NewToolResultText(string(r)), nil
	})

	// Start the server
	if err := server.ServeStdio(s); err != nil {
		fmt.Printf("Server error: %v\n", err)
	}
}

type Product struct {
	Name        string
	Price       float64
	Description string
	URL         string
}

func fetchProducts(db *sql.DB, productType string, minPrice, maxPrice float64, limit *int64) ([]Product, error) {
	var rows *sql.Rows
	var err error

	baseQuery := `
        SELECT product_name, product_price, product_description, product_url
        FROM product_data
        WHERE product_type = $1 AND product_price BETWEEN $2 AND $3
        ORDER BY product_price ASC
    `

	if limit != nil {
		baseQuery += " LIMIT $4"
		rows, err = db.Query(baseQuery, productType, minPrice, maxPrice, limit)
	} else {
		rows, err = db.Query(baseQuery, productType, minPrice, maxPrice)
	}

	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var products []Product
	for rows.Next() {
		var p Product
		if err := rows.Scan(&p.Name, &p.Price, &p.Description, &p.URL); err != nil {
			return nil, err
		}
		products = append(products, p)
	}

	return products, nil
}
