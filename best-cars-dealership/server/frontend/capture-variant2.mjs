// Genuine headful Chromium screenshots for Coursera peer-assessed Variant 2.
// Browser navigates to the real public deployment and real Django API responses.
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const base = (process.env.DEPLOY_URL || '').replace(/\/$/,'');
const out = resolve(process.cwd(), '../../evidence_variant2');
if (!base.startsWith('https://')) throw Error('DEPLOY_URL is required');
mkdirSync(out,{recursive:true});
const username = 'peer_review_' + (process.env.GITHUB_RUN_ID || Date.now());
const password = 'Demo!Pass' + (process.env.GITHUB_RUN_ID || Date.now()) + 'Qx';
const browser = await chromium.launch({headless:false,args:['--no-sandbox','--window-size=1380,860']});
const context = await browser.newContext({viewport:{width:1300,height:750},acceptDownloads:true});
const page = await context.newPage();

async function shot(name) {
  await page.bringToFront();
  await page.waitForTimeout(750);
  const location = resolve(out,name + '.png');
  execFileSync('scrot',['-u',location]);
  console.log('Captured real deployed page',name,page.url());
}
async function visit(path, locator) {
  await page.goto(base+path,{waitUntil:'domcontentloaded',timeout:110000});
  if(locator) await locator().waitFor({timeout:60000});
  await page.waitForTimeout(350);
}
try {
  await visit('/',()=>page.locator('article').first());
  await shot('get_dealers');

  await visit('/static/About.html',()=>page.getByRole('heading',{name:'About Us'}));
  await shot('about_us');
  await visit('/static/Contact.html',()=>page.getByRole('heading',{name:'Contact Us'}));
  await shot('contact_us');

  await visit('/register',()=>page.getByRole('heading',{name:'Sign-up'}));
  await shot('sign-up');
  await page.locator('#username').fill(username);
  await page.locator('#first_name').fill('Demo');
  await page.locator('#last_name').fill('Reviewer');
  await page.locator('#email').fill(username+'@example.invalid');
  await page.locator('#password').fill(password);
  await page.getByRole('button',{name:'Register'}).click();
  await page.waitForURL('**/login',{timeout:20000});
  await page.getByLabel('Username').fill(username);
  await page.getByLabel('Password').fill(password);
  await page.getByRole('button',{name:'Login'}).click();
  await page.getByText('Hi, '+username).waitFor({timeout:25000});
  await page.getByRole('link',{name:'Post Review'}).first().waitFor({timeout:20000});
  await shot('login');
  await shot('get_dealers_loggedin');

  await page.locator('select').selectOption('Kansas');
  await page.locator('article').first().waitFor();
  await shot('dealersbystate');

  await visit('/dealer/1',()=>page.getByRole('link',{name:'Post Review'}));
  await shot('dealer_id_reviews');

  await visit('/dealer/1/review',()=>page.getByRole('heading',{name:'Post Review'}));
  const review = 'Great customer service during this demo purchase '+(process.env.GITHUB_RUN_ID||Date.now());
  await page.getByLabel('Review details').fill(review);
  await page.getByLabel('Purchase date').fill('2026-10-20');
  await page.getByLabel('Car make').fill('Toyota');
  await page.getByLabel('Car model').fill('Camry');
  await page.getByLabel('Car year').fill('2023');
  await page.getByLabel('Rating (1–5)').fill('5');
  await shot('dealerhip_review_submission');
  await shot('dealership_review_submission');
  await page.getByRole('button',{name:'Publish Review'}).click();
  await page.getByText(review,{exact:true}).waitFor({timeout:20000});
  await shot('added_review');

  // Same real Django endpoints used by the deployed application.
  for (const [filename,path] of [
    ['dealer_review','/fetchReviews/dealer/1'],
    ['dealerships','/fetchDealers'],
    ['dealer_details','/fetchDealer/1'],
    ['kansasDealers','/fetchDealers/Kansas'],
    ['cars','/djangoapp/get_cars'],
    ['sentiment_analyzer','/analyze/Fantastic%20services']
  ]) {
    await visit(path,()=>page.locator('body'));
    const text = await page.locator('body').innerText();
    if(!text || text.startsWith('<!doctype html>')) throw Error('No visible API data: '+path);
    await shot(filename);
  }
  await visit('/',()=>page.locator('article').first());
  await page.getByRole('button',{name:'Logout'}).click();
  await page.getByRole('alert').getByText('You have successfully logged out.').waitFor({timeout:15000});
  await shot('logout');
  writeFileSync(resolve(out,'deploymentURL.txt'),base+'\n');
} finally {
  await browser.close();
}
