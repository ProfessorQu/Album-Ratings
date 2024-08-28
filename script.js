document.addEventListener("mousemove", event => {
    const documents = document.getElementsByClassName("cover-image");
    for (let i = 0; i < documents.length; i++) {
        documents.item(i).querySelector('img').style.transform = `perspective(1000px) rotateY(0deg) rotateX(0deg) scale3d(1, 1, 1)`;
    }

    if (event.target.tagName !== "IMG" && event.target.tagName !== "A") {
        return
    }

    const { top, bottom, left, right } = event.target.getBoundingClientRect();

    const middleX = (right + left) / 2;
    const middleY = (bottom + top) / 2;

    const {clientX, clientY} = event;

    const offsetX = (clientX - middleX) / middleX;
    const offsetY = (middleY - clientY) / middleY;

    const transformStyle = `perspective(1000px)
    rotateY(${offsetX * 10}deg)
    rotateX(${offsetY * 10}deg)
    scale3d(1, 1, 1)`;
    if (event.target.tagName === "IMG") {
        event.target.style.transform = transformStyle;
    } else {
        event.target.querySelector('img').style.transform = transformStyle;
    }
})