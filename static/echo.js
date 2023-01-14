$(document).ready(function () {
  console.log("jQuery initialized.");
});

function interactive(action, instance, csrf) {
  $.ajax({
    type: "POST",
    url: "/",
    data: {
      csrfmiddlewaretoken: csrf,
      post: instance,
      action: action,
    },
    dataType: "json",
    success: function (data) {
      console.log(data);
      if (data["status"] == "liked") {
        $(`#${data.uuid}`).find(".post-like").addClass("active");
        val = Number($(`#${data.uuid}`).find(".post-like-count").text()) + 1;
        $(`#${data.uuid}`).find(".post-like-count").text(val);
      }
      if (data["status"] == "unliked") {
        $(`#${data.uuid}`).find(".post-like").removeClass("active");
        val = Number($(`#${data.uuid}`).find(".post-like-count").text()) - 1;
        $(`#${data.uuid}`).find(".post-like-count").text(val);
      }
    },
    failure: function () {
      console.log("failure");
    },
  });
}

// () => Like/Unlike //
$(".post-container").each(function (index, element) {
  $(element)
    .find(".post-like")
    .on("click", function () {
      let csrf = $(element).find('input[name="csrfmiddlewaretoken"]').val();
      let uuid = $(element).find('input[name="post-uuid"]').val();
      interactive("like", uuid, csrf);
    });
});
