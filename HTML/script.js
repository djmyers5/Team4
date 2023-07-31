function toggleComments(id) {
    var comments = document.getElementById(id)
    if (comments.style.display === "block") {
        comments.style.display = "none"
    } else {
        comments.style.display = "block"
    }
}

function toggleOptions(id) {
    var menu = document.getElementById(id)
    if (menu.style.display === "block") {
        menu.style.display = "none"
    } else {
        menu.style.display = "block"
    }
}

function replyPost(id) {
  var reply = document.getElementById(id)
  if (reply.style.display === "block") {
    reply.style.display = "none"
  } else {
    reply.style.display = "block"
  }
}

document.getElementById('submitBtn').addEventListener('click', submitReply)
function submitReply() {
  const replyBox = document.getElementById('replyBox')
  const userReply = document.getElementById('userReply')
  const replyLabel = document.createElement('label')
  replyLabel.textContent = 'Reply has been posted'

  userReply.removeChild(replyBox)
  userReply.appendChild(replyLabel)
  document.getElementById('submitBtn').style.display = 'none'
}

function LoadIndustry(industry) {

}