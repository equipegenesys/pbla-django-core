for (let i = 1; i <= object_count; i++) {
    const row = document.getElementById(`row-${i}`);

    row.addEventListener("click", () => {
        // console.log(base_url + row.cells[1].innerHTML);
        window.location.replace(base_url + row.cells[1].innerHTML);
    });
}