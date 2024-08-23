// login.js


document.addEventListener("DOMContentLoaded", init);

async function init() {
    // definition
    const inputName = document.getElementById("input-name");
    const inputPassword = document.getElementById("input-password");

    // event
    document.getElementById("btn-login").addEventListener("click", async()=>{

        const reqData = {
            name_:inputName.value,
            password_:inputPassword.value
        }
        console.log(reqData);

        const resp = await fetch("/guest/login",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify( reqData )
        });

        if(resp.ok){
            window.location.href="/admin/"
        }else{
            alert("login fail !");
        }
    });




    console.log("login.js loading complete");
}