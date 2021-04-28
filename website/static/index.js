 // takeing noteID, send Post request using fetch to delete note end point
// after response from endpoint, window is reloaded(redirect to homepage)

function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }), 
    }) .then((_res) => {
        window.location.href = "/";
    });
}
  