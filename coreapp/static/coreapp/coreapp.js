console.log(status);
for (let i = 1; i <= 2; i++) {
    const row = document.getElementById(`row-${i}`);
    if (i === 1 && status !== "Integrado") {
        row.addEventListener("click", () => {
            window.location.href = 'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=892956057366-8l5gq4f434mv20fgkh01oap0klpon5tt.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fanalytics.pbl.tec.br%2Fapi%2Finteg%2Fgdrive%2Foauthlisten&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.metadata.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.activity.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=2&prompt=consent&access_type=offline&include_granted_scopes=true';
        });
        console.log("foi no if");
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
//     var theButton = document.getElementById(btnID);
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