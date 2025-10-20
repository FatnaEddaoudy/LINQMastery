const API_URL_BOOK = "http://localhost:5104/api/Book";

// Haal alle boeken op
export async function getBooks() {
  try {
    const response = await fetch(API_URL_BOOK);
    if (!response.ok) throw new Error("Fout bij ophalen van boeken");
    return await response.json(); // <-- return the books!
  } catch (error) {
    console.error("Error in getBooks:", error);
    return []; // return empty list so frontend doesn’t crash
  }
}

// Haal één boek op via id
export async function getBookById(id) {
  try {
    const response = await fetch(`${API_URL_BOOK}/${id}`);
    if (!response.ok) throw new Error("Fout bij ophalen van boek");
    return await response.json();
  } catch (error) {
    console.error("Error in getBookById:", error);
    return null;
  }
}
