var table = document.getElementsByClassName("table");
var rows = table.item(0).rows
    // var subpath = title.toLowerCase();

for (let i = 1; i <= object_count; i++) {
    const row = table.item(0).rows.item(i);
    const id = row.children.item(0).innerHTML;
    const path = subpath + "/" + id;
    row.addEventListener("click", () => {
        // console.log(path)
        window.location.replace(path);
    })
}