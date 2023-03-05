// RETRIEVE AUTHENTICATION STATUS //
const currentUserRetrieve = $.get("/ajax/", { action: "auth" });

function currentUserStatus() {
  return currentUserRetrieve.responseJSON.status;
}

function currentUser() {
  return currentUserRetrieve.responseJSON.user;
}

// GENERATE CSRF TOKEN //
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Ajax Function Template & On-Success Responses //
function interactive(method, url, action, instance) {
  $.ajax({
    type: method,
    url: url,
    data: {
      csrfmiddlewaretoken: csrftoken,
      instance: instance,
      action: action,
    },
    dataType: "json",
    success: function (data) {
      if (data["status"] == "liked") {
        $(`#${data.uuid}`).find(".post-like").addClass("active");
        val = Number($(`#${data.uuid}`).find(".post-like-count").text()) + 1;
        $(`#${data.uuid}`).find(".post-like-count").text(val);
      }
      if (data["status"] == "unliked") {
        $(`#${data.uuid}`).find(".post-like").removeClass("active");
        val = Number($(`#${data.uuid}`).find(".post-like-count").text()) - 1;
        if (val == 0) {
          $(`#${data.uuid}`).find(".post-like-count").text("");
        } else {
          $(`#${data.uuid}`).find(".post-like-count").text(val);
        }
      }
      if (data["status"] == "posts_retrieved") {
        removePosts();
        renderPosts(data);
      }
      if (data["status"] == "post_retrieved") {
        renderPosts(data);
        $(".post-reply-count").click()
      }
      if (data["status"] == "replies_retrieved") {
        renderPosts(data);
      }
      if (data["status"] == "followed") {
        $(".profile-follow").text("unfollow");
        $(".profile-follow").attr("class", "profile-unfollow");
        val = Number($(".profile-followers-count").text());
        $(".profile-followers-count").text(val + 1);
      }
      if (data["status"] == "unfollowed") {
        $(".profile-unfollow").text("follow");
        $(".profile-unfollow").attr("class", "profile-follow");
        val = Number($(".profile-followers-count").text());
        $(".profile-followers-count").text(val - 1);
      }
    },
    failure: function () {
      console.log("failure");
    },
  });
}

function searchEcho(instance, model, query, constraints = "default") {
  $.ajax({
    type: "GET",
    url: "/search/",
    data: {
      csrfmiddlewaretoken: csrftoken,
      model: model,
      query: query,
      constraints: constraints
    },
    dataType: "json",
    success: function (data) {
      if (instance == "message") {
        $(".user-search-results").children().remove();
        if (data["users"] == "no results") {
          $(".user-search-results").append(`
          <div class="null-result">No users matching query</div>
          `)
        } else {
          for (let user of data["users"]) {
            $(".user-search-results").append(`
            <div class="user-search-result">
              <div class="user-search-avatar"><img src="${user.avatar}" /></div>
              <div class="user-search-username">${user.username}</div>
            </div>
            `)
          }
        }
      }
    },
    failure: function () {
      console.log("failure");
    },
  });
}


// Remove Rendered Posts //
function removePosts() {
  if (document.querySelector(".post-container")) {
    currentPosts = document.querySelectorAll(".post-container");
    for (let post of currentPosts) {
      post.parentElement.remove();
    }
  }
}

// Render Fetched Posts & Replies //
function renderPosts(data) {
  if (data["status"] == "replies_retrieved") {
    $(".post-reply-form").remove();
  }

  for (let post of data["post_list"]) {
    let object = post["object"];
    let user = post["echouser"];
    let userID = post["echouser_id"];
    let avatar = post["avatar"];
    let postID = post["post_id"];
    let content = post["post"];
    let whenPosted = post["when_posted"];
    let numLikes = post["num_likes"];
    let numReplies = post["num_replies"];
    let numReposts = post["num_reposts"];
    let liked = post["liked"];

    let replyToName = post["reply_to_name"];
    let replyToID = post["reply_to_id"];

    let repostID = post["repost_id"];
    let repostAvatar = post["repost_avatar"];
    let repostUser = post["repost_user"];
    let repostPost = post["repost_post"];
    let repostTime = post["repost_time"];

    if (object == "reply") {
      replyToName = `<div class="post-reply-to">Reply<span>@</span>${post["reply_to_name"]}</div>`;
    } else {
      replyToName = "";
    }

    if (data["status"] == "replies_retrieved") {
      $(`#${replyToID}`).closest("form").after(`
          <div class='reply-container'>
            ${replyToName}

            <div class='post-avatar'>
              <img class='post-avatar-img' onclick="location.href='/users/profile/${userID}';" src="${avatar}">
            </div>
            <div class='post-body' onclick="location.href='/posts/${postID}/';">
              <div class='post-source'>
                <div class='post-user'>${user}</div>
                <div class='post-date'>${whenPosted}</div>
                <input type="hidden" name='post-uuid' value="${postID}">
              </div>
              <div class='post-content'>
                <p>${content}</p>
              </div>
            </div>
            <form class='post-actions-form'>
              <div class='post-actions' id="${postID}">
                <div class='post-reply'>
                  <div class='post-reply-icon'>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M205 34.8c11.5 5.1 19 16.6 19 29.2v64H336c97.2 0 176 78.8 176 176c0 113.3-81.5 163.9-100.2 174.1c-2.5 1.4-5.3 1.9-8.1 1.9c-10.9 0-19.7-8.9-19.7-19.7c0-7.5 4.3-14.4 9.8-19.5c9.4-8.8 22.2-26.4 22.2-56.7c0-53-43-96-96-96H224v64c0 12.6-7.4 24.1-19 29.2s-25 3-34.4-5.4l-160-144C3.9 225.7 0 217.1 0 208s3.9-17.7 10.6-23.8l160-144c9.4-8.5 22.9-10.6 34.4-5.4z"/>
                    </svg>
                  </div>
                </div>
                <div class='post-reply-count'>${numReplies}</div>
                <div class='post-repost'>
                  <div class="post-repost-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 576 432"><path d="M272 416c17.7 0 32-14.3 32-32s-14.3-32-32-32H160c-17.7 0-32-14.3-32-32V192h32c12.9 0 24.6-7.8 29.6-19.8s2.2-25.7-6.9-34.9l-64-64c-12.5-12.5-32.8-12.5-45.3 0l-64 64c-9.2 9.2-11.9 22.9-6.9 34.9s16.6 19.8 29.6 19.8l32 0 0 128c0 53 43 96 96 96H272zM304 96c-17.7 0-32 14.3-32 32s14.3 32 32 32l112 0c17.7 0 32 14.3 32 32l0 128H416c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9l64 64c12.5 12.5 32.8 12.5 45.3 0l64-64c9.2-9.2 11.9-22.9 6.9-34.9s-16.6-19.8-29.6-19.8l-32 0V192c0-53-43-96-96-96L304 96z"/>
                    </svg>
                  </div>
                </div>
                <div class="post-repost-count">${numReposts}</div>
                <div class="post-like${liked}">
                  <div class="post-like-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/>
                    </svg>
                  </div>
                </div>
                <div class="post-like-count">${numLikes}</div>
              </div>
            </form>
          </div>
        `);
    }

    if (data["status"] == "posts_retrieved" || data["status"] == "post_retrieved") {
      $("section").append(`
          <div class='section-container'>
            <div class='post-container'>

              ${replyToName}

              <div class='post-avatar'>
                <img class='post-avatar-img' onclick="location.href='/users/profile/${userID}';" src="${avatar}">
              </div>

              <div class='post-body' onclick="location.href='/posts/${postID}/';">
                <div class='post-source'>
                  <div class='post-user'>${user}</div>
                  <div class='post-date'>${whenPosted}</div>
                  <input type="hidden" name='post-uuid' value="${postID}">
                </div>
                <div class='post-content'>
                  <p>${content}</p>
                </div>
              </div>

              <form class='post-actions-form'>
                <div class='post-actions' id="${postID}">
                  <div class='post-reply'>
                    <div class='post-reply-icon'>
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M205 34.8c11.5 5.1 19 16.6 19 29.2v64H336c97.2 0 176 78.8 176 176c0 113.3-81.5 163.9-100.2 174.1c-2.5 1.4-5.3 1.9-8.1 1.9c-10.9 0-19.7-8.9-19.7-19.7c0-7.5 4.3-14.4 9.8-19.5c9.4-8.8 22.2-26.4 22.2-56.7c0-53-43-96-96-96H224v64c0 12.6-7.4 24.1-19 29.2s-25 3-34.4-5.4l-160-144C3.9 225.7 0 217.1 0 208s3.9-17.7 10.6-23.8l160-144c9.4-8.5 22.9-10.6 34.4-5.4z"/>
                      </svg>
                    </div>
                  </div>

                  <div class='post-reply-count'>${numReplies}</div>

                  <div class='post-repost'>
                    <div class="post-repost-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 576 432"><path d="M272 416c17.7 0 32-14.3 32-32s-14.3-32-32-32H160c-17.7 0-32-14.3-32-32V192h32c12.9 0 24.6-7.8 29.6-19.8s2.2-25.7-6.9-34.9l-64-64c-12.5-12.5-32.8-12.5-45.3 0l-64 64c-9.2 9.2-11.9 22.9-6.9 34.9s16.6 19.8 29.6 19.8l32 0 0 128c0 53 43 96 96 96H272zM304 96c-17.7 0-32 14.3-32 32s14.3 32 32 32l112 0c17.7 0 32 14.3 32 32l0 128H416c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9l64 64c12.5 12.5 32.8 12.5 45.3 0l64-64c9.2-9.2 11.9-22.9 6.9-34.9s-16.6-19.8-29.6-19.8l-32 0V192c0-53-43-96-96-96L304 96z"/>
                      </svg>
                    </div>
                  </div>

                  <div class="post-repost-count">${numReposts}</div>

                  <div class="post-like${liked}">
                    <div class="post-like-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 576 512"><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/>
                      </svg>
                    </div>
                  </div>

                  <div class="post-like-count">${numLikes}</div>
                </div>
              </form>
            </div>
          </div>
        `);
    }
    if (object == "repost") {
      $(`input[value='${postID}']`).closest(".post-body").append(`
          <a class="repost-link" href="/posts/${repostID}/">
            <div class="repost-container">

              <div class="repost-avatar">
                <img src="${repostAvatar}"/>
              </div>

              <div class="repost-source">
                <div class="repost-user">${repostUser}</div>
                <div class="repost-time">${repostTime}</div>
              </div>

              <div class="repost-content">
                <p>${repostPost}</p>
              </div>
            </div>
          </a>
        `);
    }
  }
}

// click() => Generate Reply Textbox //
$(document).on("click", ".post-reply", function () {
  if (currentUserStatus() == "user") {
    $(".post-reply-form").each(function (index, element) {
      $(element).remove();
    });
    postID = $(this).closest(".post-actions")[0].id;
    $(this).closest("form").after(`
        <form class='post-reply-form' action="/posts/newpost/" method="POST">
          <textarea class='post-reply-box' name="post" maxlength="280" placeholder='Write your reply here...' autocomplete="off" autofocus required></textarea>
          <input name="reply_to" type="hidden" value="${postID}">
          <input name="csrfmiddlewaretoken" type="hidden" value="${csrftoken}">
          <input id='post-reply-submit' type='submit' value='Reply'>
        </form>
      `);
  } else {
    location.href = "/accounts/login/?next=/";
  }
});

// click() => Get Post Replies //
$(document).on("click", ".post-reply-count:not(.active)", function () {
  $container = $(this).closest(".post-container");
  $(".post-container").not($container).children(".reply-container").remove();
  $(".post-container")
    .not($container)
    .find(".post-reply-count.active")
    .removeClass("active");
  $(this).addClass("active");
  let method = "GET";
  let url = "/ajax/";
  let action = "get_post_replies";
  let instance = $(this).closest(".post-actions")[0].id;
  interactive(method, url, action, instance);
});

// click() => Generate Repost Box //
$(document).on("click", ".post-repost", function () {
  if (currentUserStatus() == "user") {
    $(".post-reply-form").each(function (index, element) {
      $(element).remove();
    });
    $(".post-repost-form").each(function (index, element) {
      $(element).remove();
    });
    let repostAvatar = $(this)
      .closest(".post-container")
      .find(".post-avatar")
      .clone();
    let repostContent = $(this)
      .closest(".post-container")
      .find(".post-body")
      .clone();
    postID = $(this).closest(".post-actions")[0].id;
    $(this).closest("form").after(`
        <form class='post-repost-form' action="/posts/newpost/" method="POST">
          <div class='post-repost-container'>
            <div id='post-repost-clone'>

            </div>
            <textarea class='post-repost-box' name="post" maxlength="280" placeholder='What do you want to say?' autocomplete="off" autofocus required></textarea>
            <input name="repost_of" type="hidden" value="${postID}">
            <input name="csrfmiddlewaretoken" type="hidden" value="${csrftoken}">
            <input id='post-repost-submit' type='submit' value='Repost'>
          </div>
        </form>
      `);
    $("#post-repost-clone").append(repostAvatar);
    $("#post-repost-clone").append(repostContent);
    $("#post-repost-clone").find(".post-avatar-img").removeAttr("onclick");
    $("#post-repost-clone").find(".post-body").removeAttr("onclick");
  } else {
    location.href = "/accounts/login/?next=/";
  }
});

// click() => Follow //
$(document).on("click", ".profile-follow", function () {
  let method = "POST";
  let url = "/ajax/";
  let action = "follow";
  let instance = location.pathname.split("/")[3];
  interactive(method, url, action, instance);
});

// click() => Unfollow //
$(document).on("click", ".profile-unfollow", function () {
  let method = "POST";
  let url = "/ajax/";
  let action = "follow";
  let instance = location.pathname.split("/")[3];
  interactive(method, url, action, instance);
});

// click() => Hide Post Replies //
$(document).on("click", ".post-reply-count.active", function () {
  $container = $(this).closest(".post-container");
  $(".post-container").not($container).children(".reply-container").remove();
  $(".post-container")
    .not($container)
    .find(".post-reply-count.active")
    .removeClass("active");
  $(this).removeClass("active");
  $(this).closest("form").parent().children(".reply-container").remove();
});

// click() => Toggle Like Status //
$(document).on("click", ".post-like", function () {
  let method = "POST";
  let url = "/ajax/";
  let action = "like";
  let uuid = $(this).closest(".post-actions")[0].id;
  interactive(method, url, action, uuid);
});

// REMOVE REPLY BOX IF CLICK OUTSIDE PARENT POST //
$(document).on("click", function (event) {
  var $target = $(event.target);
  if (
    !$target.closest(".post-container").length &&
    $(".post-reply-form").is(":visible")
  ) {
    $(".post-reply-form").remove();
  }
});

// HIDE REPOST BOX IF CLICK OUTSIDE //
$(document).on("click", ".post-repost-form", function (event) {
  var $target = $(event.target);
  if (
    !$target.closest(".post-repost-container").length &&
    $(".post-repost-form").is(":visible")
  ) {
    $(".post-repost-form").remove();
  }
});

// GET MAIN POST FEED //
if (String(location.pathname) == "/") {
  let method = "GET";
  let url = "/ajax/";
  let action = "get_feed_posts";
  let instance;
  if ($(".user-display").has(".user-link").length) {
    instance = $(".user-link").attr("href").split("/")[3];
  } else {
    instance = "guest";
  }
  interactive(method, url, action, instance);
}

// GET POST DETAIL //
if (
  location.pathname.split("/")[1] == "posts" &&
  location.pathname.split("/")[2].length == 36
) {
  let postID = String(location.pathname.split("/")[2]);
  let method = "GET";
  let url = `/posts/${postID}/`;
  let action = "get_post_detail";
  let instance = postID;
  interactive(method, url, action, instance);
}

// GET PROFILE TABS & POSTS //
if (String(location.pathname).split("/")[2] == "profile") {
  let method = "GET";
  let url = "/ajax/";
  let action = "get_profile_posts";
  let instance = $(".profile-username").text();
  interactive(method, url, action, instance);
}

$(document).on("click", ".profile-posts", function () {
  let method = "GET";
  let url = "/ajax/";
  let action = "get_profile_posts";
  let instance = $(".profile-username").text();
  interactive(method, url, action, instance);
});

$(document).on("click", ".profile-replies", function () {
  let method = "GET";
  let url = "/ajax/";
  let action = "get_profile_replies";
  let instance = $(".profile-username").text();
  interactive(method, url, action, instance);
});

$(document).on("click", ".profile-likes", function () {
  let method = "GET";
  let url = "/ajax/";
  let action = "get_profile_likes";
  let instance = $(".profile-username").text();
  interactive(method, url, action, instance);
});

/* CROP AVATAR */
function loadCropTools() {
  $(".crop-base").css({
    top: "0px",
    left: "0px",
    height: "auto",
    width: "auto",
  });
  $(".crop-direction").removeClass("active");

  let initialHeight = $(".crop-base").height();
  let initialWidth = $(".crop-base").width();

  if (initialWidth > initialHeight) {
    $(".crop-base").css({
      height: "inherit",
      width: "auto",
    });
    $(".crop-right").addClass("active");
  } else if (initialHeight > initialWidth) {
    $(".crop-base").css({
      height: "auto",
      width: "inherit",
    });
    $(".crop-down").addClass("active");
  } else {
    $(".crop-base").css({
      height: "inherit",
      width: "inherit",
    });
  }

  let dimensions = Math.min(initialWidth, initialHeight);
  $(".crop-base").attr({
    dimensions: dimensions,
    initialheight: initialHeight,
    initialwidth: initialWidth,
  });

  let newWidth = $(".crop-base").width();
  let newHeight = $(".crop-base").height();
  let newDimensions = Math.min(newWidth, newHeight);
  $(".crop-save-width").val(newWidth);
  $(".crop-save-height").val(newHeight);
  $(".crop-save-dimensions").val(newDimensions);
  $(".crop-save-x").val(-+$(".crop-base").css("left").split("px")[0]);
  $(".crop-save-y").val(-+$(".crop-base").css("top").split("px")[0]);
}

/* click() -> Move Right | Crop Reticle */
$(document).on("pointerdown", ".crop-right.active", function (e) {
  const rangeX = Math.floor($(".crop-base").width() - $(".crop-image").width());
  $(".crop-left").addClass("active");

  let intervalID = setInterval(function () {
    let currentLeft = Number($(".crop-base").css("left").split("px")[0]);
    if (-currentLeft < rangeX) {
      $(".crop-base").css("left", `${currentLeft - 1}px`);
    } else {
      $(".crop-save-x").val(-+$(".crop-base").css("left").split("px")[0]);
      clearInterval(intervalID);
      $(".crop-right").removeClass("active");
    }
  }, 5);

  $(document).on("pointerup", function () {
    $(".crop-save-x").val(-+$(".crop-base").css("left").split("px")[0]);
    clearInterval(intervalID);
  });
});

/* click() -> Move Left | Crop Reticle */
$(document).on("pointerdown", ".crop-left.active", function (e) {
  $(".crop-right").addClass("active");

  let intervalID = setInterval(function () {
    let currentLeft = Number($(".crop-base").css("left").split("px")[0]);
    if (currentLeft < 0) {
      $(".crop-base").css("left", `${currentLeft + 1}px`);
    } else {
      $(".crop-save-x").val(-+$(".crop-base").css("left").split("px")[0]);
      clearInterval(intervalID);
      $(".crop-left").removeClass("active");
    }
  }, 5);

  $(document).on("pointerup", function () {
    $(".crop-save-x").val(-+$(".crop-base").css("left").split("px")[0]);
    clearInterval(intervalID);
  });
});

/* click() -> Move Down | Crop Reticle */
$(document).on("pointerdown", ".crop-down.active", function (e) {
  const rangeY = Math.floor(
    $(".crop-base").height() - $(".crop-image").height()
  );
  $(".crop-up").addClass("active");

  let intervalID = setInterval(function () {
    let currentTop = +$(".crop-base").css("top").split("px")[0];
    if (-currentTop < rangeY) {
      $(".crop-base").css("top", `${currentTop - 1}px`);
    } else {
      clearInterval(intervalID);
      $(".crop-save-y").val(-+$(".crop-base").css("top").split("px")[0]);
      $(".crop-down").removeClass("active");
    }
  }, 5);

  $(document).on("pointerup", function () {
    $(".crop-save-y").val(-+$(".crop-base").css("top").split("px")[0]);
    clearInterval(intervalID);
  });
});

/* click() -> Move Up | Crop Reticle */
$(document).on("pointerdown", ".crop-up.active", function (e) {
  $(".crop-down").addClass("active");

  let intervalID = setInterval(function () {
    let currentTop = Number($(".crop-base").css("top").split("px")[0]);
    if (currentTop < 0) {
      $(".crop-base").css("top", `${currentTop + 1}px`);
    } else {
      clearInterval(intervalID);
      $(".crop-save-y").val(-+$(".crop-base").css("top").split("px")[0]);
      $(".crop-up").removeClass("active");
    }
  }, 5);

  $(document).on("pointerup", function () {
    $(".crop-save-y").val(-+$(".crop-base").css("top").split("px")[0]);
    clearInterval(intervalID);
  });
});

/* Sign-up Avatar Preview & Crop */
$(document).on("change", ".login-avatar", function () {
  let file = this.files[0];
  try {
    $(".login-avatar-path").attr("value", file.name);
  } catch {
    $(".login-avatar-path").removeAttr("value");
    $(".crop-container").removeClass("active");
  }
  reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function (e) {
    $(".crop-base").attr("src", this.result);
  };
  reader.onerror = function (e) {
    console.log(e);
  };
  $(".crop-container").addClass("active");
});


/* USER SEARCH - MESSAGES */
$(document).on("input", ".chat-user-search", function () {
  if (!$(".user-search-results").length) {
    $(".chat-user-search").after(`
      <div class='user-search-results message' style="top: ${
        $(".chat-user-search").height() + $(".chat-user-search").offset().top
      }px">
      </div>
    `);
  }
  if ($(".chat-user-search").val().length == 0) {
    $(".user-search-results").remove();
  } else {
    let instance = "message";
    let model = "users";
    let query = $(this).val();
    searchEcho(instance, model, query);
  }
})

/* click() => close search results if click outside */
if (location.pathname.split("/")[1] == "chat") {
  $(document).on("click", function (e) {
    let $container = $(".chat-to");
    if (!$container.is(e.target) && $container.has(e.target).length === 0) {
      $(".user-search-results").remove()
      $(".chat-user-search").val(null)
    } 
  });
}

/* click() => Get or Create Private Chat */
$(document).on("click", ".user-search-result", function (event) {
  let $target = $(event.target);
  $user = $target.closest(".user-search-result");
  let username = $user.find(".user-search-username").text();

  $.post("/chat/", {
    csrfmiddlewaretoken: csrftoken,
    recipient: username,
  })
    .done(function (data) {
      let uuid = data['chat_uuid']
      location.pathname = `/chat/${uuid}/`
    });
});

/* click() => Send private message to user */
$(document).on("click", ".message-send", function () {
  if ($(".message-write-input").val() == false) {
    return false
  }
  $.post("/chat/ajax/", {
    csrfmiddlewaretoken: csrftoken,
    action: "post_message",
    chat: $(".chat-uuid").val(),
    sender: currentUser(),
    receiver: $(".message-to-username").text(),
    message: $(".message-write-input").val(),
  })
    .done(function (data) {
      $(".message-dialogue").children().remove();
      for (let message of data["messages"]) {
        if (message['sender'] === true) {
          $(".message-dialogue").append(`
          <div class='message-sent-container'>
            <div class='message-sent'>
              ${message["content"]}
            </div>
            <div class="message-timestamp">${message["timestamp"]}</div>
          </div>
          `)
        } else {
          $(".message-dialogue").append(`
          <div class="message-received-container">
            <div class="message-received">
              ${message["content"]}
            </div>
            <div class="message-timestamp">${message["timestamp"]}</div>
          </div>
          `)
        }
      }
      $(".message-dialogue-container").scrollTop($(".message-dialogue").height());
      $(".message-write-input").val('');
    })
});

/* click() -> GENERATE ARTICLE COMMENT FORM */
$(document).on("click", ".article-comment-icon", function () {
  if (currentUserStatus() == "user") {
    if ($(".article-comment-form").length) {
      $(".article-comment-icon").removeClass("active")
      $(".article-comment-form").remove()
    } else {
      $(".article-comment-icon").addClass("active")
      $(".post-reply-form").each(function (index, element) {
        $(element).remove();
      });
      $(".post-repost-form").each(function (index, element) {
        $(element).remove();
      });
      $(".article-container").after(`
        <form action="${location.pathname}" method="post" class="article-comment-form">
          <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
          <input type="hidden" name="type" value="comment">
          <div class="article-comment-container">
            <textarea name="post" class="article-comment-write"></textarea>
            <input type="submit" value="Comment" class="article-comment-submit">
          </div>
        </form>
      `);
    }
  } else {
    window.location.pathname = "/accounts/login/";
  }
})

/* click() -> GENERATE ARTICLE SHARE FORM */
$(document).on("click", ".article-share-icon", function () {
  if (currentUserStatus() == "user") {
    $(".post-reply-form").each(function (index, element) {
      $(element).remove();
    });
    $(".post-repost-form").each(function (index, element) {
      $(element).remove();
    });
    $(".article-comment-form").remove()
    $(".article-comment-icon").removeClass("active")
    $("section").append(`
      <form class="article-share-form" method="post" action="${location.pathname}">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
        <input type="hidden" name="type" value="share">
        <div class="article-share-container">
          <div class="article-share-card">
            <img class="article-share-image" src="${$(".article-image > img").attr("src")}" alt="Article Image"/>
            <div class="article-share-detail">
              <div class="article-share-title">${$(".article-title").text()}</div>
              <div class="article-share-source">${$(".article-source").text()}</div>
            </div>
          </div>

          <textarea class="article-share-write" name="post" maxlength="280" placeholder="Write your message here.."></textarea>
          <input type="submit" value="Share" class="article-share-send">
        </div>
      </form>
    `);
  } else {
    window.location.pathname = "/accounts/login/";
  }
})

/* REMOVE ARTICLE SHARE BOX IF CLICK OUTSIDE */
$(document).on("click", ".article-share-form", function (event) {
  var $target = $(event.target);
  if (
    !$target.closest(".article-share-container").length &&
    $(".article-share-form").is(":visible")
  ) {
    $(".article-share-form").remove();
  }
});