function setupPublicChatWebSocket(debug_mode, room_id) {
  /**
   * Setup the websocket tasked with dealing with chat data.
   */
    // Correctly decide between ws:// and wss://
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  if (debug_mode === true) {
    var ws_path = ws_scheme + "://" + window.location.host + `/public_chat/${room_id}/`;
  } else {
    var ws_path = ws_scheme + "://" + window.location.host + `:8001/public_chat/${room_id}/`;
  }
  var public_chat_socket = new WebSocket(ws_path);

  // Handle incoming messages
  public_chat_socket.onmessage = function (message) {
    console.log("Got chat websocket message " + message.data);
    var data = JSON.parse(message.data);
    appendChatMessage(data)
  };

  public_chat_socket.addEventListener("open", function (e) {
    console.log("Public ChatSocket OPEN")
    createChatElement("<i>You're connected to the chat.</i>")
  })

  public_chat_socket.onclose = function (e) {
    console.error("Public ChatSocket closed.");
    createChatElement("<i>You've been disconnected from the chat. Refresh the page to try and rejoin.</i>")
  };

  public_chat_socket.onOpen = function (e) {
    console.log("Public ChatSocket onOpen", e)
  }

  public_chat_socket.onerror = function (e) {
    console.log("Public ChatSocket error", e)
  }

  if (public_chat_socket.readyState == WebSocket.OPEN) {
    console.log("Public ChatSocket OPEN")
  } else if (public_chat_socket.readyState == WebSocket.CONNECTING) {
    console.log("Public ChatSocket connecting..")
  }

  document.getElementById("id_chat_message_input").focus();
  document.getElementById("id_chat_message_input").onkeyup = function (e) {
    if (e.keyCode === 13 && e.shiftKey) {  // enter + return
      // Handled automatically
    } else if (e.keyCode === 13 && !e.shiftKey) { // enter + !return
      document.getElementById("id_chat_message_submit").click();
    }
  };

  document.getElementById("id_chat_message_submit").onclick = function (e) {
    const messageInputDom = document.getElementById("id_chat_message_input");
    const message = messageInputDom.value;
    public_chat_socket.send(JSON.stringify({
      "command": "send",
      "message": message
    }));
    messageInputDom.value = "";
  };
}

function appendChatMessage(data) {
  /**
   * Define all chat related data and append it before creating the chat message element.
   */
  let message = data["message"]
  let fullName = data["full_name"]
  let text = `<b>${fullName}</b>: ${message}`;
  createChatElement(text)
}

function createChatElement(text) {
  /**
   * Create the chat text element allowing all chat related data to be displayed to the chat log.
   */

  var chatLog = document.getElementById("id_chat_log")

  var newMessageDiv = document.createElement("div")
  newMessageDiv.classList.add("d-flex")
  newMessageDiv.classList.add("flex-row")

  var div1 = document.createElement("div")
  div1.classList.add("d-flex")
  div1.classList.add("flex-column")

  var message = document.createElement("p")
  message.innerHTML = text
  div1.appendChild(message)

  newMessageDiv.appendChild(div1)

  chatLog.insertBefore(newMessageDiv, chatLog.lastChild)
  chatLog.scrollTop = chatLog.scrollHeight;
}

document.getElementById("id_chat_message_input").addEventListener("keydown", function (e) {
  if (e.keyCode === 13) {
    document.getElementById("id_chat_message_submit").click()
  }
});