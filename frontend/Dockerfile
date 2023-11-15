# Use an official Node.js runtime as the base image for the builder stage
FROM node:14-buster-slim AS builder

# Set the working directory for the React project
WORKDIR /payroll-system/frontend

# Copy package.json and package-lock.json for dependencies installation
COPY package.json package-lock.json ./

# Install application dependencies
RUN npm install

# Copy the entire project into the container
COPY . .

# Build the React application
RUN npm run build

# Create a production image to serve the built files
FROM nginx:alpine

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the Nginx configuration file for your app
COPY nginx.conf /etc/nginx/conf.d/

# Copy the built files from the builder stage to the Nginx webroot
COPY --from=builder /payroll-system/frontend/dist /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80
