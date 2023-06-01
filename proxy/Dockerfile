# Base image
FROM nginx

WORKDIR /Back/proxy/

COPY nginx.conf /Back/proxy/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]