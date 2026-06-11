const { createElement } = require("react");

async function loadPosts(){
    const res = await fetch("../posts.json");
    const posts = await res.json();
    
    const contentDiv = document.getElementById("contentDiv");

    for (var i = 0; i < posts.length; i++){
        element = document.createElement("a");
        element.innerHTML = posts[i]["title"];
        element.href = posts[i]["url"];

        contentDiv.appendChild(element)
    }
}