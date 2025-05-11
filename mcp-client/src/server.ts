import express from "express";
import cors from "cors";
import MCPClient from "./mcpClient.js";

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

app.post("/product/search", async (req, res) => {
  const mcpClient = new MCPClient();
  try {
    await mcpClient.connectToServer();

    const response = await mcpClient.processQuery(req.body.query);

    let suggestions = [];

    const suggestionsStartIndex = response.indexOf('{"suggestions":');

    if (suggestionsStartIndex !== -1) {
      const jsonStr = response.slice(suggestionsStartIndex).trim();

      try {
        const parsed = JSON.parse(jsonStr);
        suggestions = parsed.suggestions;
      } catch (e) {
        console.error("Failed to parse JSON:", e);
      }
    } else {
      console.error("No valid JSON object with 'suggestions' found.");
    }

    res.status(200).json({ products: suggestions, message: null });
  } catch (e) {
    console.error("error occured", e);
    res.status(500).json({ products: [], message: "error occured" });
  } finally {
    await mcpClient.cleanup();
  }
});

app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
