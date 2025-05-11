import express from "express";
import MCPClient from "./mcpClient.js";

const app = express();
const PORT = 3000;

app.use(express.json());

app.post("/product/search", async (req, res) => {
  const mcpClient = new MCPClient();
  try {
    await mcpClient.connectToServer();
    const response = await mcpClient.processQuery(req.body.query);
    res.status(200).json({ response });
  } catch (e) {
    console.error("error occured", e);
    res.status(500).json({ response: "error occured" });
  } finally {
    await mcpClient.cleanup();
  }
});

app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
