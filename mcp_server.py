from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name = "read_doc_contents",
    description = "Read the contents of a document given its id"
)
def read_doc_contents(doc_id: str = Field(..., description="The id of the document to read")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs.get(doc_id)

@mcp.tool(
    name = "edit_docucment",
    description = "Edit the contents of a document given its id and new contents"
)
def edit_document(
    doc_id: str = Field(..., description="The id of the document to edit"),
    old_str: str = Field(..., description="The string to be replaced in the document"),
    new_str: str = Field(..., description="The string to replace the old string with in the document")
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    doc_contents = docs.get(doc_id)
    if old_str not in doc_contents:
        raise ValueError(f"String '{old_str}' not found in document with id '{doc_id}'.")
    updated_contents = doc_contents.replace(old_str, new_str)
    docs[doc_id] = updated_contents
    return updated_contents
# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
