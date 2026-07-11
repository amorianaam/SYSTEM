const mysql = require('mysql2/promise');
require('dotenv').config();

const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT) || 4000, 
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'orthocare_db',
  waitForConnections: true,
  connectionLimit: 50, 
  queueLimit: 0,      
  enableKeepAlive: true,
  keepAliveInitialDelay: 10000, 
  ssl: {
    rejectUnauthorized: true 
});

(async () => {
  try {
    const connection = await pool.getConnection();
    console.log('🚀 [TiDB Cloud] Connection established and secured successfully with SSL!');
    connection.release();
  } catch (error) {
    console.error('❌ [Database Error] Connection to TiDB Cloud failed:', error.message);
  }
})();

module.exports = pool;
