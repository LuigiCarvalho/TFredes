import java.net.InetAddress;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;

public class TabelaRoteamento {
    /*Implemente uma estrutura de dados para manter a tabela de roteamento. 
     * A tabela deve possuir: IP Destino, Métrica e IP de Saída.
    */
    public class entradasTabela{
        public String ipDestino;
        public int metrica;
        public String ipSaida;

        public entradasTabela(String ipDestino, int metrica, String ipSaida){
            this.ipDestino = ipDestino;
            this.metrica = metrica;
            this.ipSaida = ipSaida;
        }

        public void setIpDestino(String ipDestino){
            this.ipDestino = ipDestino;
        }

        public void setMetrica(int metrica){
            this.metrica = metrica;
        }

        public void setIpSaida(String IpSaida){
            this.ipSaida = ipSaida;
        }
    }

    public ArrayList<entradasTabela> routerTable;
    public ArrayList<String> vizinhos;
    //******************************************************/   
    
    public TabelaRoteamento(){
        routerTable = new ArrayList<>();
        vizinhos = new ArrayList<>();

        /* Le arquivo de entrada com lista de IPs dos roteadores vizinhos. */
        try ( Scanner inputFile = new Scanner(new File("IPVizinhos.txt"))) {
            String ip;

            while(inputFile.hasNextLine()){
                ip = inputFile.nextLine();
                vizinhos.add(ip);
                routerTable.add(new entradasTabela(ip, 1, ip));
            }
            
        } catch (FileNotFoundException ex) {
            System.out.println("Deu merda, arquivo n encontrado");
            return;
        }
    }
    
    
    public void update_tabela(String tabela_s,  InetAddress IPAddress){
        /* Atualize a tabela de rotamento a partir da string recebida. */
        tabela_s = "*192.168.1.2;1*192.168.1.3;1"; //teste
        
    
    }
    
    public String get_tabela_string(){
        String tabela_string = "";
        if(routerTable.size()==0){
           return "!"; /* Tabela de roteamento vazia conforme especificado no protocolo */
        }
        /* Converta a tabela de rotamento para string, conforme formato definido no protocolo . */
        
        return tabela_string;
    }
    

    
}
