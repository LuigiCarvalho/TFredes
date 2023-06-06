public class Roteador {

    public static void main(String[] args){
        
        /* Cria instâncias da tabela de roteamento e das threads de envio e recebimento de mensagens. */
        TabelaRoteamento tabela = new TabelaRoteamento();
        Thread sender = new Thread(new MessageReceiver(tabela));
        Thread receiver = new Thread(new MessageSender(tabela, tabela.vizinhos));
        
        sender.start();
        receiver.start();
        
    }
    
}
