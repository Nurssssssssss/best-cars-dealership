import {chromium} from 'playwright';
import {execFileSync} from 'node:child_process';
import {mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
const base='http://127.0.0.1:5173';
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
}finally{await browser.close();}
