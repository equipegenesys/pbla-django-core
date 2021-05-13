for (let i = 1; i <= object_count; i++) {
    const row = document.getElementById(`row-${i}`);

    row.addEventListener("click", () => {
        // console.log(row.cells[2].innerHTML);
        window.location.replace("turmas/" + row.cells[2].innerHTML + "/equipes");
    });
}