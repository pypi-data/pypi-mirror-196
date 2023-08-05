const max_cards = 250
var ws = new WebSocket("ws://localhost:8004/ws")

const createCard = data => {
    const card = document.createElement('div')
    card.classList.add('card')
    card.innerHTML = event.data
    return card
}

ws.onmessage = function(event) {
    const card = createCard(event.data)
    const cards = document.getElementById('cards')
    const lastCard = cards.firstChild
    cards.insertBefore(card, lastCard)
    if (cards.childNodes.length > max_cards) {
        cards.removeChild(cards.lastChild)
    }

}

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
