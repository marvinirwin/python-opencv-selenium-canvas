def create_image(driver, base64png, title):
    str = """
    try {
        debugger;
        const title = document.createElement('h3');
        title.text = arguments[0];
        document.body.appendChild(title);
        
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${arguments[1]}`;
        document.body.appendChild(img);
    }
    catch(e) {
        console.log(e);
    }
    """
    driver.execute_script(
        str,
        title,
        base64png
    )