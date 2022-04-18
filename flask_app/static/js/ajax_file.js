console.log("File run successfully upon loading page for first time");  

function get_one_pool_staff(id){
    fetch(`http://127.0.0.1:5000/pool/${id}/ajax`)
    .then(response => response.json()) // Take data from HTML response object and extract JSON)
    .then(data => {
        var allStaff = document.getElementById("all-staff");
        allStaff.innerHTML = "";
        var row = document.createElement("div");
        row.setAttribute("class","row");
        // If no data found
        if (data.length == 0) {
            allStaff.innerHTML += "<h1>No staff found.</h1>"
        } else {
            // Loop through staff for this pool - if we have any
            if (data[0]["id"] == undefined || data[0]["id"] == null) {
                allStaff.innerHTML += `<p class="fs-3">Staff: None found</p>`;
            } else { // Loop through each staff
                allStaff.innerHTML += `<p class="fs-3 text-center">Staff for this pool</p>`;
                var newList = document.createElement("ul");
                newList.setAttribute("class","staff-list")
                for (var k = 0; k < data.length; k++) { // Each row is a dictionary/
                    newList.innerHTML += `<li>${data[k]["first_name"]} ${data[k]["last_name"]}</li>`;
                }
                allStaff.appendChild(newList);
            }
        }
    })
}
