const submit=document.getElementById("submit");
const submit_l=document.getElementById("submit_l")

if(submit_l){
    submit_l.addEventListener(("click"),async ()=>{
        const username=document.getElementById("username_l").value;
        const password=document.getElementById("password_l").value;
        const data = await login(username,password);
        if(data && data.result){
            localStorage.setItem('token', data.result);
            window.location.href = './profile.html';
        } else if(data){
            alert(data.message || 'Login failed');
        }
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
    submit.addEventListener("click", async ()=>{
        const email=document.getElementById("email").value;
        const passwd=document.getElementById("password").value;
        const data = await register(email, passwd);
        if(data && data.token){
            localStorage.setItem('token', data.token);
            window.location.href = './profile.html';
        } else if(data){
            alert(data.error || 'Registration failed');
        }
    });
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
            const errorData = await res.json();
            console.error('Registration failed:', errorData);
            alert(`Registration failed: ${errorData.error || 'Unknown error'}`);
            throw new Error(`HTTP ${res.status}: ${errorData.error || 'Registration failed'}`);
        }
        
        const responseData = await res.json();
        console.log('Registration successful:', responseData);
        alert('Organizer registration successful!');
        return responseData;
    }catch(e){
        console.error('Registration error:', e);
        if (!e.message.includes('HTTP')) {
            alert('Registration failed. Please check your internet connection and try again.');
        }
    }
}
