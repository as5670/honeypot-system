fetch("../data.json")
    .then(response => response.json())
    .then(data => {

        // Total attempts
        document.getElementById("total").innerText = data.total_attempts;

        // Find top username
        let max = 0;
        let topUser = "-";

        for (let user in data.usernames) {
            if (data.usernames[user] > max) {
                max = data.usernames[user];
                topUser = user;
            }
        }

        document.getElementById("topUser").innerText = topUser;

        // List usernames
        let list = document.getElementById("userList");

        for (let user in data.usernames) {
            let li = document.createElement("li");
            li.innerText = `${user} → ${data.usernames[user]} attempts`;
            list.appendChild(li);
        }

    })
    .catch(err => {
        console.log("Error loading data.json", err);
    });
