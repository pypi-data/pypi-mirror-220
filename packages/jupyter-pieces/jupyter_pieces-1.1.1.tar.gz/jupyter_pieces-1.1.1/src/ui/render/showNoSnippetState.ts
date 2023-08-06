import { ClassificationSpecificEnum } from '../../PiecesSDK/connector';
import { returnedSnippet } from '../../typedefs';
import { constructSnippet } from '../views/renderListView';
import { addLogo } from './addLogo';

export function showNoSnippetState(container: HTMLDivElement) {
    container.innerHTML = '';

    let stateContainer = document.createElement('div');
    stateContainer.classList.add('pieces-empty-state');

    addLogo(stateContainer);

    let firstLine = document.createElement('p');
    firstLine.innerText =
        "You're so close to getting started! Try saving this code snippet!";
    stateContainer.appendChild(firstLine);

    let snippetConstraint = document.createElement('div');
    snippetConstraint.classList.add('snippetConstraint');

    //Switch out this stringified Piece code for new JSON if you want to change the default snippet
    const snippetRaw = [
        'class HelloWorld:',
        '    def __init__(self):',
        '        self.message = "Hello, World!"',
        '',
        '    def say_hello(self):',
        '        print(self.message)',
        '',
        '# Create an instance of the class',
        'hello = HelloWorld()',
        '',
        '# Call the say_hello method',
        'hello.say_hello()',
    ];
    const snippetTotal = snippetRaw.join('\n');

    const snippet: returnedSnippet = {
        title: 'Hello World Snippet',
        id: '',
        type: '',
        raw: snippetTotal,
        language: ClassificationSpecificEnum.Py,
        time: '',
        created: new Date(),
        description:
            'A simple "Hello World" Snippet that shows you how to use Pieces!',
        updated: new Date(),
        share: undefined,
    };

    let testPiece = constructSnippet(snippet, true);
    snippetConstraint.appendChild(testPiece);

    container.appendChild(stateContainer);
    stateContainer.appendChild(snippetConstraint);
}
