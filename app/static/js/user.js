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

const submit_organizer=document.getElementById("submit_organizer");
if(submit_organizer){
    submit_organizer.addEventListener("click",(e)=>{
        e.preventDefault();       
        const orgData = {
            org_name: document.getElementById("org_name").value,
            org_type: document.getElementById("org_type").value,
            org_description: document.getElementById("org_description").value,
            contact_name: document.getElementById("contact_name").value,
            contact_position: document.getElementById("contact_position").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
            confirm_password: document.getElementById("confirm_password").value
        };
        
        return registerOrganizer(orgData);
    })
}
async function registerOrganizer(data){
    try{
        const res=await fetch("http://127.0.0.1:5000/auth/register_organizer",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(data)
        }); 
        if(!res.ok){
            throw new Error("Problem in user.js");
        }
        const responseData = await res.json();
        return responseData;
    }catch(e){
        console.log(e);
    }
}
