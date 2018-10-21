//http://www.academia.edu/12084461/Research_of_using_Homomorphic_Filtering_Function_to_fix_non-_uniform_of_illumination
#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <thread>
#include <fstream>
#include <sstream>
#include <map>

using namespace std;

// representação de um ponto (local: escola, casa do aluno ou do motorista) na cidade
struct No
{
  float x,y; 
  char tipo; 
  int escola;

  // construtor vazio
  No(){}

  // constroi nó com base na localização, tipo de endereço e ID da escola
  No(float x, float y, char tipo, int escola)
  {
    this->x = x;
    this->y = y;
    this->tipo = tipo;
    this->escola = escola;
  }
};

class Grafo
{
private:
  // grafos formados por nós que se interconectam
  vector<vector<float>> grafo; // grafo : informa o peso entre todos os seus pontos (locais)
  vector<vector<int>> escolas; // escolas: informa a qual escola pertence cada aluno, além do nó que a representa (sendo esse o index 0)
  vector<No> nos; // número de locais do grafo
  int num_nos = 0;
  int num_escolas = 0;

public:
  Grafo() {}

  // grafo responsável pela criação das rotas possíveis para o motorista
  Grafo(string nome_arquivo)
  {
    string linha, dado;
    ifstream entrada(nome_arquivo); // abre o arquivo contendo os dados de todos os pontos escolhidos no mapa
    char tipo;
    ofstream myfile("final.txt"); // arquivo onde será salva a melhor rota para o motorista

    while (getline(entrada, linha)) // peca cada linha do arquivo de entrada e processa 
    {
      stringstream ss(linha); // pega a linha e armazena em ss
      while (ss >> dado) // lê primeiro caractere da linha 
      {
        if (dado == "m") // verifica se é um motorista
        {
          tipo = dado.c_str()[0]; // tipo = 'm'
          this->grafo.push_back(vector<float>()); // adiciona um nó ao grafo
          this->escolas.push_back(vector<int>(1, 0)); // adiciona um nó com valor 0 ao grafo
          this->num_escolas++; 
        }
        else if (dado == "e") // verifica se é uma escola
        {
          tipo = dado.c_str()[0]; // tipo = 'e'
          this->grafo.push_back(vector<float>()); // adiciona um nó ao grafo
          this->escolas.push_back(vector<int>()); 
          this->escolas.back().push_back(this->num_nos); // indexa a escola qual o nó que ela representa no grafo
          this->num_escolas++; // icrementa o número de escolas
        }
        else if (dado == "c") // verifica se é um aluno
        {
          tipo = dado.c_str()[0]; // tipo = 'c'
          this->grafo.push_back(vector<float>());
          this->escolas.back().push_back(this->num_nos); // indexa a escola qual o aluno que ela contém 
        }
        else if (dado == "d") // informa que os próximos dados correspondem as distâncias entre o ponto avaliado e os outros locais
        {
          while (ss >> dado) // ler cada distância e arasena no grafo 
          {
            this->grafo.at(this->num_nos).push_back(stof(dado));
          }
          this->num_nos++;
        }
        else if (dado == "p") // informa que os próximos dados correspondem a localização do ponto
        {
          ss >> dado; 
          float x = stof(dado); // pega a coordenada x do local
          ss >> dado;
          float y = stof(dado); // pega a coordenada y do local
          myfile << x << ", " << y << endl;
          // adiciona um novo local, informando qual o tipo do local, a sua localização e 
          this->nos.push_back(No(x, y, tipo, this->escolas.back().at(0)));
        }
      }
    }
    entrada.close();
    myfile << endl;
    myfile.close();
  }

  // construtor por cópia
  Grafo(const Grafo &G)
  {
    this->num_nos = G.num_nos;
    this->nos = G.nos;
    this->escolas = G.escolas;
    this->grafo = G.grafo;
  }

  // gerar um grafo de forma aleatória com base nos intervalos [0,range_x] e [0,range_y] com 'numero_nos' nós 
  Grafo(const int &numero_nos, const int range_x, const int range_y)
  {
    ofstream myfile;
    myfile.open("inicial.txt"); // abrir arquivo para salvar os resultados 
    char tipo = 'm'; // tipo a despresar 
    this->num_nos = numero_nos;
    this->grafo = vector<vector<float>>(numero_nos, vector<float>(numero_nos));

    //Gerando valores de x e y aleatórios para cada No
    float x, y;

    for (int i = 0; i < numero_nos; i++)
    {
      x = (float)rand() / RAND_MAX * range_x;
      y = (float)rand() / RAND_MAX * range_y;
      this->nos.push_back(No(x, y, tipo, 0)); // adiciona o nó no grafo 
      myfile << nos.at(i).x << " - " << nos.at(i).y << endl; // posições salvas no grafo 
    }

    myfile.close();

    //Calculando distancia euclidiana para cada no
    for (int i = 0; i < numero_nos; i++)
    {
      for (int j = 0; j < numero_nos; j++)
      {
        // grafo[i][j] = sqrt(x^2 + y^2)
        this->grafo.at(i).at(j) = sqrt(pow(this->nos.at(i).x - this->nos.at(j).x, 2.0) + pow(this->nos.at(i).y - this->nos.at(j).y, 2.0));
      }
    }
  }

  // retorna a distância entre dois locais 
  float getPeso(const int no1, const int no2)
  {
    return grafo.at(no1).at(no2);
  }

  // retorna o número de locais do grafo
  int getNumNos()
  {
    return num_nos;
  }

  // retorna o número de escolas do grafo
  int getNumEscolas()
  {
    return num_escolas;
  }

  // retorna os dados das escolas
  vector<vector<int>> getEscolasAlunos()
  {
    return escolas;
  }

  // verifica se todos os alunos estão presentes na escola informada dado o seu ID e sua a quantidade de alunos
  bool todosAlunosPresentes(const int &tam_al, const int &id_escola)
  {
    // procura a escola
    for (int i = 0; i < num_escolas; i++)
    {
      if (escolas.at(i).at(0) == id_escola && tam_al == (escolas.at(i).size() - 1))
      {
        return true; // informa que todos os alunos estão presentes
      }
    }
    return false; // informa que nem todos os alunos estão presentes
  }

  // retorna o tipo do nó que tem ID == valor
  char getTipo(const int &valor)
  {
    return nos.at(valor).tipo;
  }

  // forma a URL que será interpretada pelo pelo browser de acordo com os padrões da API do Bing
  void printURL(vector<int> caminho)
  {
    ofstream myfile;
    myfile.open("link.txt");
    ostringstream s; 
    string url = "http://bing.com/maps/default.aspx?rtp="; // primeira parte da url
    for (int i = 0; i < caminho.size(); i++)
    {
      s << "pos." << nos.at(caminho.at(i)).x << "_" << nos.at(caminho.at(i)).y << "~"; // armazenando posição na url 
    }
    s << "pos." << nos.at(caminho.at(0)).x << "_" << nos.at(caminho.at(0)).y << "&rtop=0~1~0"; // ligando o ponto final ao inicial
    myfile << url + s.str(); // salvando a url em arquivo (link.txt)
    myfile.close();
  }

  // imprime os detalhes do grafo no terminal
  void printGrafo()
  {
    cout << "Lista de locais: \n";
    for (int i = 0; i < num_nos; i++)
    {
      // imprime cada elemento ligado a um determinado nó separados por ','
      for (vector<float>::iterator it = grafo.at(i).begin(); it != grafo.at(i).end(); ++it)
      {
        cout << *it << ", ";
      }
      cout << endl;
    }

    cout << "Lista de alunos: ";
    for (int i = 0; i < num_escolas; i++)
    {
      cout << "* escola " << i << ": ";
      // imprime o ID de cada aluno contido na escola 'i' separados por vírgula 
      for (vector<int>::iterator it = escolas.at(i).begin(); it != escolas.at(i).end(); ++it)
      {
        cout << *it << ", ";
      }
      cout << endl;
    }
  }
};

// classe responsável pelo Algoritmo Genético
class GA 
{
private:
  Grafo graph; // grafo que será usado para descrever todos os caminhos possíveis entre dois locais
  int tam_pop = 10; // tamanho da população, que por padão é 10
  const int torneio_num = 3; // método utilizado na seleção: torneio com 3 elementos competindo
  vector<vector<int>> pop; // população formada por um vetor contendo o ID de cada local por onde o motorista vai passar 
  vector<int> best; // melhor caminho 
  float best_peso; // distância total do melhor caminho (menor distância)

  // algoritmo que gera aleatoriamente a população inicial 
  void gerarPopulacaoInicial()
  {
    //Número de nós do grafo
    int q_nos = this->graph.getNumNos(); 

    // pega todas as escolas do grafo
    vector<vector<int>> escola_alunos = this->graph.getEscolasAlunos();

    // deleta a primeira escola da lista de escolas 
    escola_alunos.erase(escola_alunos.begin());

    // inicia o a melhor distância com um valor muito alto, 
    // de modo que será substituído pelo primeiro caminho que encontrar 
    this->best_peso = 5000; 


    for (int i = 0; i < this->tam_pop; ++i)
    {

      vector<vector<int>> e_a = escola_alunos;
      // vetor contendo um caminho inicial
      vector<int> cromossomo;

      // embaralha os elementos (IDs dos alunos) contido em cada 'linha' das escolas e_a
      // perceba que o primeiro elemento do vetor e_a é tirado 
      for (int j = 0; j < e_a.size(); j++)
      {
        random_shuffle(e_a.at(j).begin() + 1, e_a.at(j).end()); // embaralhando 'e_a.at(j)'
      }

      // inicial o cromossomo (caminho) com a posição 0
      cromossomo.push_back(0); 

      // formação do cromossomo inicial (caminho inical)
      // passa pela casa de todos os alunos 
      while (!e_a.empty())
      {
        int p = rand() % e_a.size(); // pega aleatoriamente uma posição de uma escola
        if (!e_a.at(p).empty())  
        {
          cromossomo.push_back(e_a.at(p).back()); // adiciona o último aluno da escola no cromossomo
          e_a.at(p).pop_back(); // retira o último aluno da escola
        }
        else
        {
          e_a.erase(e_a.begin() + p); // retira a escola, caso ela não contenha os alunos 
        }
      }

      // atualiza o melhor caminho
      if (fitness(cromossomo) < best_peso)
      {
        best = cromossomo; // melhor caminho
        best_peso = fitness(cromossomo); // menor distância
      }
      this->pop.push_back(cromossomo); // inclui o melhor caminho na população 
    }
  }

  // retorna a distância total do caminho, dado o cromossomo (caminho) como parâmentro
  float fitness(const vector<int> &crom)
  {
    int tam = crom.size();
    float sum = 0.0; // distância
    for (int i = 1; i < tam; ++i) 
    {
      sum += (float)this->graph.getPeso(crom[i - 1], crom[i]); // peso entre as casas dos indivídos 'i' e 'i-1'
    }
    // peso entre o último local do caminho e o início do caminho (fechar o ciclo)
    sum += (float)this->graph.getPeso(crom[tam - 1], crom[0]); 
    return sum; // retorna a distância total
  }

  // método de seleção do algoritmo utilizando TORNEIO
  vector<vector<int>> selecao() // argumento: probabilidade de 
  { 
    vector<vector<int>> popChild; // população de pais selecionados
    vector<vector<int>> torneio; // população selecionada aleatoriamente a cada iteração

    // gera uma população 'popChild' de mesmo tamanho da população inicial
    for (int i = 0; i < tam_pop; ++i)
    {
      //Seleciona aletóriamente cromossomos para torneio
      int melhor = 0;
      float best_fit = 100000, fit = 0;

      for (int j = 0; j < torneio_num; j++)
      {
        //Obtem um cromossomo aleatório
        torneio.push_back(this->pop[rand() % tam_pop]); 
        fit = fitness(torneio.at(j)); // calcula o fitness do cromossomo selecionado 

        //Escolhe melhor dos vetores escolhidos do torneio
        if (best_fit > fit || j == 0)
        {
          melhor = j; // posição do melhor indivíduo do torneio 
          best_fit = fit;
        }
      }

      popChild.push_back(torneio.at(melhor)); // adiciona o indivíduo que ganhou o torneio 

      torneio.clear(); // limpa o vetor de indivídos que competem no torneio 
    }
    return popChild; // retorna a população selecionada
  }

  // verifica se o 'valor' (representa o ID de uma criança) já está contido no cromossomo 'comaparar', 
  // iterando até o valor 'fim'
  bool estaRepetido(const int &valor, const vector<int> &comparar, const int fim)
  {
    map<int, int> esc;
    for (int i = 1; i < fim; i++)
    {
      // caso o nó a ser analizado seja uma escola, tem que verificar se todos os alunos já estão no vetor 'comaparar'
      if (this->graph.getTipo(valor) == 'e')
      {
        esc[comparar.at(i)] += 1; // adiciona mais uma aluno na posição 'comparar.at(i)' da escola
        // verifica se todos os alunos estão presentes e se o nó 'valor' representa a escola da posição 'i'
        if (comparar.at(i) == valor && !this->graph.todosAlunosPresentes(esc[comparar.at(i)], comparar.at(i)))
        {
          return true;
        }
      }
      else
      {
        //se for aluno, não precisa verifiar se da certo ou não, só se está repetido
        if (comparar.at(i) == valor)
        {
          return true;
        }
      }
    }
    return false;
  }

  // gera a nova população após cruzar os elementos
  vector<vector<int>> cruzarDados(vector<vector<int>> p_parents)
  {
    vector<vector<int>> n_pop; // população a ser gerada
    
    int crom_size = graph.getNumNos(); // pega quantidade de nós 
    for (int i = 0; i < this->tam_pop - 1; i += 2) // percorre toda a população 
    {
      // pega dois cromossomos vizinhos a cada iteração
      // esses cromossomos serão armazenados no 'n_pop' após serem processados
      vector<int> crom1 = p_parents[i];
      vector<int> crom2 = p_parents[i + 1];

      int no;
      //preenche segunda metade do primeiro cromossomo com informações do segundo cromossomo
      for (int j = crom_size / 2; j < crom_size; j++)
      {
        //Vai verificando a cada posição do segundo cromossomo se já ta repetido no primeiro
        //Se está repetido, vai na segunda posição e assim por diante
        int k = 1;
        do
        {
          no = crom2.at(k);
          k++;
        } while (estaRepetido(no, crom1, j));

        crom1.at(j) = no;
      }
      // preenche segunta metade do segundo cromossomo com informações do primeiro cromossomo
      for (int j = crom_size / 2; j < crom_size; j++)
      {
        // verifica a cada elemento da posição k do cromossomo 'crom1' se este já está contido na primeira metade do cromossomo 'crom2'
        // caso esteja, itera k e repete-se o processo. Caso contrário, armazena na posição 'j' de crom2 o ID da criança
        int k = 1;
        do
        {
          no = crom1.at(k);
          k++;
        } while (estaRepetido(no, crom2, j));

        crom2.at(j) = no;
      }

      // armazena os cromossomos an nova população 
      n_pop.push_back(crom1);
      n_pop.push_back(crom2);
    }

    return n_pop; // retorna a nova população 
  }

  // apenas verifica se o aluno 'aluno' está contido na escola 'escola'
  bool pertenceaEscola(const int &aluno, const int &escola)
  {
    int n_escolas = graph.getNumEscolas(); // quantidade de escolas
    vector<vector<int>> escolas = graph.getEscolasAlunos(); // escolas

    // varrer as escolas até encontrar a escola de ID 'escola'
    for (int k = 0; k < n_escolas; k++)
    {
      if (escolas.at(k).at(0) == escola) // verifica se é a escola procurada
      {
        // varre os alunos da escola procurando o aluno 'aluno'
        for (int j = 1; j < escolas.at(k).size() - 1; k++) 
        {
          if (escolas.at(k).at(j) == aluno) // retorna 'true' caso o aluno seja encontrado na escola
            return true;
        }
      }
    }
    return false; // retorna 'false' caso o aluno não seja encontrado na escola
  }

  // faz a mutação dos 'p_parents' cromossomos a uma determinada taxa 'taxa'
  void mutacao(vector<vector<int>> &p_parents, float taxa)
  {
    int size = p_parents.size(); // quantidade de pais
    int q_nos = graph.getNumNos(); // quantidade de nós 
    int tentativas = 0; 
    int p1, p2;
    for (int i = 1; i < size; ++i) // varre todos os cromossomos do vetor 'p_parents'
    {
      // caso o valor aleatório gerado seja menor que a taxa, o cromossomo sofrerá mutação
      if ((float)rand() / RAND_MAX < taxa) 
      {
        // faz sucessívas tentantivas até fazer a primeira mutação no cromossomo | número de cromossomos igual a 10
        while (tentativas < 10) 
        {
          p1 = rand() % (q_nos - 1) + 1; // sorteia uma posição aleatória 

          p2 = pow(-1, rand() % 2); // sorteria -1 ou 1 para 

          if (p1 == 1)
          {
            p2 = 1;
            // verifica se ao lado direito da posição sorteada há uma escola 
            if (graph.getTipo(p_parents[i][p1 + 1]) == 'e') 
            {
              // verifica se o aluno da posição p1 pertence a escola que se encontra na posição p1+1
              if (!pertenceaEscola(p_parents[i][p1], p_parents[i][p1 + 1]))
                break; // caso não pertença, pode fazer a mutação 
              else
                tentativas++; // caso contrário, tenta novamente
            }
            else
              break; // se não for uma escola, pode fazer a mutação normalmente 
          }
          // verifica se o elemento selecionado é o último local do cromossomo
          else if (p1 == q_nos - 1)
          {
            p2 = -1;
            // caso o elemento do lado esquerdo do elemento selecionado da posição selecionada seja um aluno
            if (graph.getTipo(p_parents[i][p1 - 1]) == 'c')
            {
              // caso o aluno (p1 - 1) não esteja contido na escola
              if (!pertenceaEscola(p_parents[i][p1 - 1], p_parents[i][p1]))
                break; // pode haver mutação
              else
                tentativas++; // esteja contido, não haverá mutação 
            }
            else
              break; // caso o elemento não seja um aluno, pode haver a mutação 
          }
          else // posição selecionada do cromossomo não é nem o primeiro elemento e nem o último 
          {
            // verifica se o elemento selecionado é uma escola
            if (graph.getTipo(p_parents[i][p1]) == 'e')
            {
              // caso o elemento do seu lado (selecionado com base no sorteio de p2) seja também uma escola, pode haver a mutação 
              if ((graph.getTipo(p_parents[i][p1 + p2]) == 'e'))
              {
                break;
              }
              // verifica se o elemento do seu lado é um aluno 
              else if (graph.getTipo(p_parents[i][p1 + p2]) == 'c')
              {
                // se o elemento é um aluno e está no lado direito da escola, pode haver a mutação 
                if (p2 == 1)
                  break;
                else // lado esquerdo 
                {
                  // verifica se o aluno está contido na escola da posição p1
                  if (!pertenceaEscola(p_parents[i][p1 + p2], p_parents[i][p1]))
                    break; // se sim, pode fazer a mutação 
                  else
                    tentativas++; // tentar novamente
                }
              }
            }
            // verifica se o elemento selecionado é um aluno 
            else if (graph.getTipo(p_parents[i][p1]) == 'c')
            {
              // caso o seu vizinho seja um aluno, pode haver a mutação 
              if ((graph.getTipo(p_parents[i][p1 + p2]) == 'c'))
              {
                break;
              }
              // verifica se seu vizinho é uma escola 
              else if (graph.getTipo(p_parents[i][p1 + p2]) == 'e')
              {
                // se esse vizinho for o da esquerda, poderá haver a mutação 
                if (p2 == -1)
                  break;
                else
                {
                  // se o elemento não está contido na escola da direita, pode haver mutação 
                  if (!pertenceaEscola(p_parents[i][p1], p_parents[i][p1 + 1]))
                    break;
                  else
                    tentativas++; // caso esteja, não poderá haver mutação 
                }
              }
            }
          }
        }

        // ocorre a mutação no indivíduo/cromossomo
        // trocasse os indivíduos das posições 'p1' e 'p1+p2'
        int aux = p_parents[i][p1];
        p_parents[i][p1] = p_parents[i][p1 + p2];
        p_parents[i][p1 + p2] = aux;
      }
    }
  }

  // atualiza qual o melhor inivíduo da população
  // percorretodos os elementos da população atrás do melhor 
  void atualizarBest()
  {
    best_peso = fitness(this->pop[0]); 
    for (int i = 1; i < this->tam_pop; ++i)
    {
      if (fitness(this->pop[i]) < best_peso)
      {
        this->best = this->pop[i];
        this->best_peso = fitness(this->pop[i]);
      }
    }
  }

  // salva em arquivo o melhor caminho encontrado e mostra dados sobre o processamento dos dados 
  void imprimirBest(vector<int> popi, bool arquivo)
  {
    ofstream myfile; // arquivo 
    if (arquivo)
    {
      myfile.open("final.txt", ios_base::app); // abre o arquivo 'final.txt'
    }

    cout << "\nMelhor caminho: fitness = " << this->best_peso << "\n rota: ";
    int size = popi.size(); // tamanho do caminho 
    // percorre todos os indivíduos do cromossomo 
    for (int i = 0; i < size; ++i)
    {
      // caso a variável 'arquivo' seja 'true', salva em arquivo o melhor caminho. 
      // Caso contrário, mostra na tela 
      if (arquivo)
      {
        myfile << popi[i]; 
        if (i != size - 1)
          myfile << "->";
      }
      else
      {
        cout << popi[i];
        if (i != size - 1)
          cout << "->";
      }
    }
    // fecha arquivo 
    if (arquivo)
    {
      myfile.close();
    }
  }

 

public:
  // construtor do Algoritmo Genético, passando o grafo e o tamanho da população 
  GA(const Grafo &G, int tam_pop = 10)
  {
    this->graph = Grafo(G); // grafo a ser trabalhado 
    this->tam_pop = tam_pop; // população para iterações do GA
  }

  // principal algoritmo: onde todo o procedimento é feito, desde a geração da população até a impressão dos resultados na tela 
  void algoritmo(int num_it)
  {
    int contIt = 0;
    this->gerarPopulacaoInicial(); // gerando uma nova população 

    while (contIt++ < num_it) // iterando até que o número de iterações seja alcançado 
    {
      vector<vector<int>> pop_sel = selecao(); // seleciona os indivíduos da atual população 
      vector<vector<int>> pop_children = cruzarDados(pop_sel); // cruza os dados desses indivíduos retornando uma nova população 
      mutacao(pop_children, 0.02); // produz mutações em cada cromossomo dos novos indivíduos a uma taxa de 2%
      vector<vector<int>> n_pop; // nova população 
      n_pop.reserve(pop.size());
      // a construção do ELITISMO se dá aqui, onde pegamos os dados dos melhores pais selecionados
      // juntamos com os filhos gerados pelo cruzamento de mutação da população de pais selecionados 
      n_pop.insert(n_pop.end(), pop_sel.begin(), pop_sel.end());
      this->pop = n_pop; // subistitui a população gerada, pela população antiga
      atualizarBest(); // calcula qual o melhor cromossomo da nova população 
    }

    imprimirBest(this->best, true); // imprime qual o melhor cromossomo no arquivo (arg2 = true)
    this->graph.printURL(this->best); // gera URL em uma arquivo, a qual colocaremos no browser para vizualisar o resultado final 
  }
};

int main()
{
  srand(time(0));
  Grafo G("output.txt"); // gera uma novo grafo
  G.printGrafo(); // mostra o grafo gerado 
  GA Teste(G, 100); // forma o GA com uma população de tamanho 100
  Teste.algoritmo(50); // dá início ao algoritmo
}
