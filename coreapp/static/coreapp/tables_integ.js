var table = document.getElementsByClassName("table");
var rows = table.item(0).rows

for (let i = 1; i <= object_count; i++) {
    const row = table.item(0).rows.item(i);
    const insti_id = row.children.item(1).innerHTML;
    const integ_id = row.children.item(3).innerHTML;
    // console.log(insti_id, integ_id)
    const path = insti_id + "/integ/" + integ_id;
    row.addEventListener("click", () => {
        // console.log(subpath)
        window.location.assign(path);
    })
}