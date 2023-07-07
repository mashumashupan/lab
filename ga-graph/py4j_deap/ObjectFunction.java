import py4j.GatewayServer;


public class ObjectFunction {

    // 目的関数: ここを書き換える
    public double obfunc(double x, double y) {

        return (x-1.0) * (x-1.0) + (y-2.0) * (y-2.0);
    }

    // javaのサーバを立てる
    public static void main(String[] args) {
        ObjectFunction app = new ObjectFunction();
        // app を gateway.entry_point に設定
        GatewayServer server = new GatewayServer(app);
        server.start();
        System.out.println("Gateway Server Started");
    }
}
