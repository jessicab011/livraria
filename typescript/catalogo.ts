import type { Livro } from "./livro.js";

export const livros: Livro[] = [
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

export function buscarLivro(titulo: string): Livro | undefined {
    return livros.find(
        (livro) => livro.titulo.toLowerCase() === titulo.toLowerCase());
}

export function cadastrarLivro(novoLivro: Livro): void {
    livros.push(novoLivro);
    console.log(`Livro "${novoLivro.titulo}" cadastrado com sucesso!`);
}

export function listarLivros(): void {
    console.log("Lista de livros disponíveis:");
    for (const livro of livros) {
        console.log(`ID: ${livro.id}, Título: ${livro.titulo}, Autor: ${livro.autor}, Preço: R$${livro.preco.toFixed(2)}, Estoque: ${livro.estoque}`);
    }
}

export function buscarLivrosPorTitulo(titulo: string): Livro[] {
    return livros.filter(
        (livro) => livro.titulo.toLowerCase().includes(titulo.toLowerCase())
    );
}
