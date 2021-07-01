var table = document.getElementsByClassName("table");
var rows = table.item(0).rows

for (let i = 1; i <= object_count; i++) {
    const row = table.item(0).rows.item(i);
    const user_id = row.children.item(1).innerHTML;
    const integ_id = row.children.item(3).innerHTML;
    // console.log(insti_id, integ_id)
    const path = user_id + "/integ/" + integ_id;
    row.addEventListener("click", () => {
        // console.log(subpath)
        window.location.assign(g_drive_integ_link);
    })
}


// console.log(g_drive_integ_link);
// for (let i = 1; i <= 2; i++) {
//     const row = document.getElementById(`row-${i}`);
//     if (i === 1 && status !== "Integrado") {
//         row.addEventListener("click", () => {
//             window.location.replace(g_drive_integ_link);
//         });
//     }
// }