const submit=document.getElementById("submit");
const submit_l=document.getElementById("submit_l")

if(submit_l){
    submit_l.addEventListener(("click"),()=>{
        const username=document.getElementById("username_l").value;
        const password=document.getElementById("password_l").value;
        return login(username,password)
    })
}


async function login(name,password){
    try{
        const res=await fetch("http://127.0.0.1:5000/auth/login",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username:name,
                password:password
            })
        })
        if(!res.ok){
            throw new Error("Problem in user.js")
        }
        const data=await res.json()
        return data
    }
    catch(err){
        console.log(err)
    }
}
async function register(name,password){
    try{
        const res=await fetch("http://127.0.0.1:5000/auth/register",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username:name,
                password:password
            })
        });
        if(!res.ok){
        throw new Error ("Problem in user.js");}
        const data=await res.json()
        return data;
    }catch(e){
        console.log(e);
    }
}
if(submit){
    submit.addEventListener("click",()=>{
    const email=document.getElementById("email").value;
    const passwd=document.getElementById("password").value;
    return register(email,passwd);
})
}
