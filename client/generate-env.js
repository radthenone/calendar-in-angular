const fs = require('fs');
const dotenv = require('dotenv');
const {resolve} = require("path");

dotenv.config(
    {
        path: resolve(__dirname, '../.env.local')
    },
);

const environment = `
export const environment = {
  frontendUrl: '${process.env.FRONTEND_URL}',
  backendUrl: '${process.env.BACKEND_URL}',
  secretKey: '${process.env.SECRET_KEY}',
  apiUrl: '${process.env.API_URL}',
};
`;

fs.writeFileSync(resolve(__dirname, './environment.ts'), environment);
