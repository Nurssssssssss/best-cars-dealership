export async function csrf(){await fetch('/api/csrf/',{credentials:'same-origin'});}
function cookie(name){return document.cookie.split('; ').find(x=>x.startsWith(name+'='))?.split('=')[1]||''}
export async function api(path,options={}){
 const method=options.method||'GET';if(method!=='GET')await csrf();
 const res=await fetch('/api/'+path,{...options,credentials:'same-origin',headers:{'Content-Type':'application/json',...(method!=='GET'?{'X-CSRFToken':decodeURIComponent(cookie('csrftoken'))}:{}),...options.headers}});
 const data=await res.json();if(!res.ok)throw Error(data.error||'Request failed');return data;
}
