let projectsURL = "http://127.0.0.1:8000/api/projects";

let getProjects = () => {
    fetch(projectsURL)
        .then(response => response.json())
        .then(data => {
            builProjects(data);
            addVoteEvents();
        })
        .catch(err => {
            console.log(err);
        })
};


let builProjects = (projects) => {
    let projectWrapper = document.getElementById("projects-wrapper");

    for (let i = 0; projects.length > i; i++) {
        let project = projects[i];
        let projectCard = `
            <div class="project-card">
                <img src="http://127.0.0.1:8000${project.featured_image}" />

                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive feedback</i>
                    <p>${project.description.substring(0,150)}</p>
                </div>
            </div>
        `
        projectWrapper.innerHTML += projectCard;
    }
};

let addVoteEvents = () => {
    let voteButtons = document.getElementsByClassName('vote--option');

    for (let i = 0; voteButtons.length > i; i++) {
        voteButtons[i].addEventListener('click', (e) => {
            let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMjA0NTQzLCJqdGkiOiI5MGQ4ZGQyOTExMjI0ZmQwODI1NjIyMWMzMmRlYTBjMCIsInVzZXJfaWQiOjExfQ.BcbeG_0n_aVCnWD5DHJEnHedBwfRvOViKvnOImm7VhE";
            let vote = e.target.dataset.vote;
            let projectid = e.target.dataset.project;

            fetch(`http://127.0.0.1:8000/api/projects/${projectid}/vote/`, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        'value': vote
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("success");

                })
                .catch(error => console.log(error))
        });
    }
}

getProjects();