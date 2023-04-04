form = document.getElementById("login_form");
if (form != null) {
  form.addEventListener("submit", (e) => {
    console.log(true);
    e.preventDefault();
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let data = {
      username: username,
      password: password,
    };
    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        window.location.href = "/";
        console.log(response);
      } else {
        console.log(response);
      }
    });
  });
}
signup_form = document.getElementById("signup_form");
if (signup_form != null) {
  signup_form.addEventListener("submit", (e) => {
    e.preventDefault();
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let name = document.getElementById("name").value;
    let phn = document.getElementById("phn").value;
    let password = document.getElementById("password").value;

    let data = {
      username: username,
      email: email,
      name: name,
      phn: phn,
      password: password,
    };
    fetch("/api/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        window.location.href = "/login";
        console.log(response);
      } else {
        console.log(response);
      }
    });
  });
}
user_post = document.getElementById("postcard");
if (user_post != null) {
  user_post.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(user_post);
    fetch("/api/posts", {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (response.ok) {
        // here add code to fetch the new post and add it to the feed
        // window.location.href = "/login";
        console.log(response);
      } else {
        console.log("not ok");
      }
    });
  });
}
function logout() {
  fetch("/api/logout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/login";
    } else {
      console.log(response);
    }
  });
}
follow_form = document.getElementById("follow_form");
if (follow_form != null) {
  follow_form.addEventListener("submit", (e) => {
    e.preventDefault();
    let follow_user = document.getElementById("follow_user").value;
    let btn = document.getElementById("follow-btn");
    let data = {
      follow_user: follow_user,
      follow_toggle: btn.value,
    };
    fetch("/api/follow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        if (btn.value == "Follow") {
          btn.value = "Unfollow";
        } else {
          btn.value = "Follow";
        }
        console.log(response.data);
        console.log(response.body);
      } else {
        console.log(response.text());

        console.log(response.message);

        console.log(response.status);
      }
    });
  });
}

// user search api
username_input = document.getElementById("username-input");
if (username_input != null) {
  display_username = document.getElementById("display-username");

  username_input.addEventListener("keyup", (e) => {
    if (username_input.value == "") {
      while (display_username.firstChild) {
        display_username.removeChild(display_username.firstChild);
      }
    } else {
      fetch(`/api/user/${username_input.value}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          while (display_username.firstChild) {
            display_username.removeChild(display_username.firstChild);
          }
          for (let i = 0; i < data.length; i++) {
            // const para = document.createElement("p");
            // para.textContent = `${data[i].username}`;
            // display_username.appendChild(para);
            display_username.innerHTML += `<div class="card mb-3" style="max-width: 540px">
            <div class="row g-0">
              <div class="col-md-4">
                <img
                  src="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"
                  class="img-fluid rounded-start"
                  alt="avatar"
                />
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title"><a href="/${data[i].username}">${data[i].username}</a></h5>
                  <p class="card-text" style="font-size: 0.8em;">${data[i].name}</p>
                </div>
              </div>
            </div>
          </div>`;
          }
        });
    }
  });
}

// edit profile
if (
  window.location.pathname == "/settings" ||
  window.location.pathname == "/settings/edit_profile"
) {
  edit_profile = document.getElementById("edit_profile");
  function editProfile() {
    for (let i = 0; i < edit_profile.elements.length; i++) {
      edit_profile[i].removeAttribute("disabled");
    }
  }
  edit_profile.addEventListener("submit", (e) => {
    e.preventDefault();
    formData = new FormData(edit_profile);
    fetch("/api/user", {
      method: "PUT",
      body: formData,
    }).then((response) => {
      if (response.ok) window.location.href = "/settings";
      else console.log("error");
    });
  });
}

if (window.location.pathname == "/settings/delete_account") {
  delete_profile = document.getElementById("delete-account");

  delete_profile.addEventListener("click", (e) => {
    e.preventDefault();
    fetch("/api/user", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.ok) window.location.href = "/signup";
      else console.log("error");
    });
  });
}


// post like
function likePost(post_id) {
  fetch(`/api/like/${post_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.ok) {
      console.log(response);
    } else {
      console.log(response);
    }
  });
}