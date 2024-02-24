const puppeteer = require('puppeteer');
const sqlite3 = require('sqlite3').verbose();
const dbPath = '/app/blog.db'; 

async function adminLoginAndVisitReportedUrls() {

    let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
        if (err) {
            console.error('Could not connect to the database', err);
            return;
        }
        console.log('Connected to the SQLite database.');
    });

    let browser;
    try {
        browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security'] // Necessary for Docker compatibility
        });
        const page = await browser.newPage();

        try {
   
            console.log('Attempting to navigate to login page...');
            await page.goto('http://webapp:5000/login', {waitUntil: 'networkidle2'});
            console.log('Login page loaded, attempting to fill login form...');

            await page.type('#username', 'admin'); // Fill in the username.
            await page.type('#password', process.env.ADMIN_PASSWORD); // Fill in the password.

            console.log('Form filled, attempting to submit...');
            // Start waiting for navigation before clicking the submit button.
            const navigationPromise = page.waitForNavigation();
            await page.click('button[type="submit"]');
            // Now, wait for the navigation to complete.
            await navigationPromise;
            
            console.log('Navigation after login detected.');

        } catch (error) {
            console.error('Login process failed:', error);
            throw error; // Rethrow to skip the rest of the process
        }
  
        await new Promise((resolve, reject) => {
            db.serialize(() => {
                db.get(`SELECT url FROM report ORDER BY id DESC LIMIT 1`, async (err, row) => {
                    if (err) {
                        console.error('Database query error:', err);
                        reject(err);
                        return;
                    }
                    if (row) {
                        console.log(`Visiting reported URL: ${row.url}`);
                        try {
                            await page.goto(row.url, {waitUntil: 'networkidle2'});
                            console.log('Navigation complete');
                            resolve();
                        } catch (e) {
                            console.error('Error visiting reported URL:', e);
                            reject(e);
                        }
                    } else {
                        console.log("No reports found.");
                        resolve();
                    }
                });
        
                db.close((err) => {
                    if (err) {
                        console.error('Error closing the database:', err.message);
                        reject(err);
                    }
                    console.log('Closed the database connection.');
                });
            });
        });

} catch (error) {
    console.error('An error occurred:', error);
} finally {
    if (browser) {
        await browser.close();
    }
}
}

setInterval(adminLoginAndVisitReportedUrls, 30000);
