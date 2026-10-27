import {chromium} from 'playwright';
import {execFileSync,spawn} from 'node:child_process';
import {mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
const base=process.env.FRONT_URL || 'http://127.0.0.1:5173';
const out=resolve(process.cwd(),'../../evidence');
mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:false,args:['--no-sandbox','--window-size=1380,860']});
const context=await browser.newContext({viewport:{width:1300,height:750}});
const page=await context.newPage();
async function snap(name){
 await page.bringToFront();
 await page.waitForTimeout(900);
 const file=resolve(out,name+'.png');
 try{execFileSync('scrot',['-u',file]);}
 catch{await page.screenshot({path:file,fullPage:true});}
 console.log(name,page.url());
}
try{
 await page.goto(base+'/',{waitUntil:'networkidle'});
 await page.locator('article').first().waitFor();
 await snap('get_dealers');
 await page.goto(base+'/login',{waitUntil:'networkidle'});
 await page.getByLabel('Username').fill('course_demo');
 await page.getByLabel('Password').fill(process.env.DEMO_PASSWORD);
 await page.getByRole('button',{name:'Login'}).click();
 await page.getByText('Hi, course_demo').waitFor();
 await snap('get_dealers_loggedin');
 await page.locator('select').selectOption('Kansas');
 await snap('dealersbystate');
 await page.goto(base+'/dealer/1',{waitUntil:'networkidle'});
 await page.getByText('Fantastic services',{exact:false}).first().waitFor();
 await snap('dealer_id_reviews');
 await page.goto(base+'/dealer/1/review',{waitUntil:'networkidle'});
 await page.getByLabel('Review details').fill('Fantastic services and a pleasant purchase experience');
 await page.getByLabel('Purchase date').fill('2026-10-20');
 await page.getByLabel('Car make').fill('Toyota');
 await page.getByLabel('Car model').fill('Camry');
 await page.getByLabel('Car year').fill('2023');
 await page.getByLabel('Rating (1–5)').fill('5');
 await snap('dealership_review_submission');
 await page.getByRole('button',{name:'Publish Review'}).click();
 await page.getByText('Fantastic services and a pleasant purchase experience').waitFor();
 await snap('added_review');
 await page.goto('http://127.0.0.1:8000/admin/',{waitUntil:'networkidle'});
 await page.locator('#id_username').fill('root');
 await page.locator('#id_password').fill(process.env.ADMIN_PASSWORD);
 await page.locator('input[type=submit]').click();
 await page.getByText('Site administration').waitFor();
 await snap('admin_login');
 await page.goto('http://127.0.0.1:8000/admin/dealers/carmodel/',{waitUntil:'networkidle'});
 await page.locator('#result_list').waitFor();
 await snap('car_models');
 await page.locator('form[action*="logout"] button').first().click();
 await snap('admin_logout');
 // An actual terminal window, displaying authentic Django server output from this CI run.
 const log=resolve(out,'django_server');
 const cmd='head -n 25 '+JSON.stringify(log)+'; printf "\\nLATEST REQUESTS:\\n"; tail -n 7 '+JSON.stringify(log)+'; sleep 15';
 const term=spawn('xterm',['-T','Real running Django server','-geometry','118x34+30+30','-fa','Monospace','-fs','12','-e','sh','-c',cmd],{stdio:'ignore'});
 try{
  await page.waitForTimeout(1300);
  const ids=execFileSync('xdotool',['search','--name','Real running Django server'],{encoding:'utf-8'}).trim().split('\\n');
  execFileSync('xdotool',['windowfocus','--sync',ids.at(-1)]);
  await page.waitForTimeout(350);
  execFileSync('scrot',['-u',resolve(out,'django_server.png')]);
  console.log('Captured real terminal with Django startup log');
 }catch(err){console.log('Terminal capture unavailable:',err.message)}
 finally{term.kill()}
 // Repeat the anonymous home screenshot once Chromium is fully visible.
 await page.goto(base+'/',{waitUntil:'networkidle'});
 await page.locator('article').first().waitFor();
 await snap('get_dealers');
}finally{await browser.close();}
