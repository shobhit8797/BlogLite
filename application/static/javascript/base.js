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
    let phn = document.getElementById("username").value;
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
    let title = document.getElementById("post_title").value;
    let content = document.getElementById("post_content").value;
    let data = {
      title: title,
      content: content,
    };
    fetch("/api/posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        // window.location.href = "/login";
        console.log(response);
      } else {
        console.log(response);
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
      follow_toggle : btn.value
    };
    fetch("/api/follow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        if(btn.value == "Follow")
        {
          btn.value = "Unfollow";
        }
        else
        {
          btn.value = "Follow";
        }
        console.log(response.data);
        console.log(response.body);
      } else {
        console.log(response);
      }
    });
  });
}