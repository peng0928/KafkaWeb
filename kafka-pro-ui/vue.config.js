module.exports = {
  devServer: {
    port: 9527,
    proxy: {
      '^/api': {
        changeOrigin: true, //开启代理： 在本地会创建一个虚拟服务端，然后发送请求数据，并且同时接收请求数据，这样客户端和服务端进行数据的交互就不会有跨域问题
        target: 'http://127.0.0.1:9528' // 要访问的跨域的域名
      }
    },
  }
};