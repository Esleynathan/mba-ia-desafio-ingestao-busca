from search import search_prompt

def main():
    print("="*50)
    print("Sistema de Busca Semântica - Chat CLI")
    print("="*50)
    print("\nDigite sua pergunta ou 'sair' para encerrar.\n")

    while True:
        try:
            question = input ("\nFaça sua pergunta:").strip()

            if question.lower() in ['sair', 'exit', 'quit', '']:
                print("\nEncerrando chat. Até logo!")
                break

            print("\nProcessando...")
            chain = search_prompt(question)
            if not chain:
                print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
                return

            print(f"\nPERGUNTA: {question}")
            print(f"RESPOSTA: {chain}\n")
            print("-"*50)
            
        except KeyboardInterrupt:
            print("\n\nEncerrando chat. Até logo!")
            break
        except Exception as e:
            print(f"\nErro: {e}")
            print("Tente novamente.\n")

if __name__ == "__main__":
    main()