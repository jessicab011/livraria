
interface Livro {
  id: number;
  titulo: string;
  autor: string;
  preco: number;
  estoque: number;
}

const livros: Livro[] = [
  {
    id: 1,
    titulo: "Dom Casmurro",
    autor: "Machado de Assis",
    preco: 29.9,
    estoque: 10,
  },
  {
    id: 2,
    titulo: "O Pequeno Príncipe",
    autor: "Antoine de Saint-Exupéry",
    preco: 24.5,
    estoque: 5,
  },
];

console.log(livros);

function buscarLivro(titulo: string): Livro | undefined {
    return livros.find(
        (livro) => livro.titulo.toLowerCase() === titulo.toLowerCase());

}

const resultado = buscarLivro("livro inexistente");

if(resultado){
    console.log("Livro encontrado:", resultado);
} else {
    console.log("Livro não encontrado");
}

function cadastrarLivro(novoLivro: Livro): void {
    livros.push(novoLivro);
    console.log(`Livro "${novoLivro.titulo}" cadastrado com sucesso!`);
}

cadastrarLivro({
    id: 3,
    titulo: "Capitães da Areia",
    autor: "Jorge Amado",
    preco: 35.9,
    estoque: 8,
});

console.log("Catálogo atualizado:", livros);

function listarLivros(): void {
    console.log("Lista de livros disponíveis:");

    for (const livro of livros) {
        console.log(`ID: ${livro.id}, Título: ${livro.titulo}, Autor: ${livro.autor}, Preço: R$${livro.preco.toFixed(2)}, Estoque: ${livro.estoque}`);
    }
}   

listarLivros();