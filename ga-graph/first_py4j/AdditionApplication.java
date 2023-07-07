import py4j.GatewayServer;


public class AdditionApplication {

    public int addition(int first, int second) {
        return first + second;
    }

    public static void main(String[] args) {
        AdditionApplication app = new AdditionApplication();
        // app を gateway.entry_point に設定
        GatewayServer server = new GatewayServer(app);
        server.start();
        // System.out.println("Gateway Server Started");
    }
}
