document.getElementById("form").onsubmit = async (e) => {

    e.preventDefault()

    let form = new FormData(e.target)

    await fetch("/add", {
        method: "POST",
        body: form
    })

    location.reload()
}

async function complete(id) {

    await fetch("/complete/" + id)

    location.reload()
}
