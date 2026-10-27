// Capture real screenshots from an already publicly deployed dealership app.
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const base=(process.env.DEPLOY_URL||'').replace(/\/$/,'');
if (!base.startsWith('https://')) throw new Error('A real HTTPS DEPLOY_URL is required');
const output=resolve(process.cwd(),'../../evidence');
mkdirSync(output,{recursive:true});
const browser=await chromium.launch({
  headless:false,args:['--no-sandbox','--window-size=1380,860']
});
const context=await browser.newContext({viewport:{width:1300,height:750}});
const page=await context.newPage();
const username='coursera_'+Date.now();
const password='DemoPass'+Date.now()+'!';
async function capture(name){
  await page.bringToFront();
  await page.waitForTimeout(900);
  execFileSync('scrot',['-u',resolve(output,name+'.png')]);
  console.log('Actual public browser screenshot:',name,page.url());
}
try{
  await page.goto(base+'/',{waitUntil:'networkidle',timeout:90000});
  await page.locator('article').first().waitFor({timeout:60000});
  await capture('deployed_landingpage');
  await page.goto(base+'/register',{waitUntil:'networkidle'});
  await page.locator('#username').fill(username);
  await page.locator('#first_name').fill('Course');
  await page.locator('#last_name').fill('Reviewer');
  await page.locator('#email').fill(username+'@example.invalid');
  await page.locator('#password').fill(password);
  await page.getByRole('button',{name:'Register'}).click();
  await page.waitForURL('**/login',{timeout:15000});
  await page.getByLabel('Username').fill(username);
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button',{name:'Login'}).click();
  await page.getByText('Hi, '+username).waitFor();
  await capture('deployed_loggedin');
  await page.goto(base+'/dealer/1',{waitUntil:'networkidle'});
  await page.getByText('Post Review').waitFor();
  await capture('deployed_dealer_detail');
  await page.goto(base+'/dealer/1/review',{waitUntil:'networkidle'});
  const review='Great service from a real deployed demo '+Date.now();
  await page.getByLabel('Review details').fill(review);
  await page.getByLabel('Purchase date').fill('2026-10-20');
  await page.getByLabel('Car make').fill('Toyota');
  await page.getByLabel('Car model').fill('Camry');
  await page.getByLabel('Car year').fill('2023');
  await page.getByLabel('Rating (1–5)').fill('5');
  await page.getByRole('button',{name:'Publish Review'}).click();
  await page.getByText(review,{exact:true}).waitFor();
  await capture('deployed_add_review');
  await page.goto(base+'/',{waitUntil:'networkidle'});
  await page.getByRole('button',{name:'Logout'}).click();
  await page.getByRole('link',{name:'Login'}).waitFor();
  await capture('deployed_landingpage');
  writeFileSync(resolve(output,'deploymentURL'),base+'\n');
}finally{await browser.close();}
