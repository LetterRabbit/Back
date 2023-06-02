# Base image
FROM --platform=linux/amd64 nginx

WORKDIR /Back/proxy/

COPY nginx.conf /Back/proxy/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]