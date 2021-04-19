// console.log(g_drive_integ_link);
for (let i = 1; i <= 2; i++) {
    const row = document.getElementById(`row-${i}`);
    if (i === 1 && status !== "Integrado") {
        row.addEventListener("click", () => {
            window.location.replace(g_drive_integ_link);
        });
    }
    // if (i === 2) {
    //     row.addEventListener("click", () => {
    //         window.location.href = '/home/estudante';
    //     });

    // }
}

// function toggle(btnID, eIDs) {
//     // Feed the list of ids as a selector
//     var theRows = document.querySelectorAll(eIDs);
//     // Get the button that triggered this
//     var theButton = document.getElementById(btnID;
//     // If the button is not expanded...
//     if (theButton.getAttribute("aria-expanded") == "false") {
//         // Loop through the rows and show them
//         for (var i = 0; i < theRows.length; i++) {
//             theRows[i].classList.add("shown");
//             theRows[i].classList.remove("hidden");
//         }
//         // Now set the button to expanded
//         theButton.setAttribute("aria-expanded", "true");
//         // Otherwise button is not expanded...
//     } else {
//         // Loop through the rows and hide them
//         for (var i = 0; i < theRows.length; i++) {
//             theRows[i].classList.add("hidden");
//             theRows[i].classList.remove("shown");
//         }
//         // Now set the button to collapsed
//         theButton.setAttribute("aria-expanded", "false");
//     }
// }