// GPT PROMPT for function parseDescription()
// There are three markers:
// 1 📝 Custom Description:
// 2 💡 Smart Description:
// 3 🔎 Suggested Searches:
// If the line following the first marker is not,
// “Write a custom description here.” Then return that line plus
// the ones following up until the second marker
// Otherwise, return the lines following the second marker,
// up until the third marker, unless the third marker does not exist,
// then just return the rest of the lines after the second marker.

export function parseDescription(input: string | undefined): string {
    if (!input) {
        return '';
    }
    const lines = input.split('\n');

    const firstMarker = '📝 Custom Description: ';
    const secondMarker = '💡 Smart Description: ';
    const thirdMarker = '🔎 Suggested Searches: ';

    const firstMarkerIndex = lines.findIndex((line) => line === firstMarker);

    const secondMarkerIndex = lines.findIndex((line) => line === secondMarker);

    if (
        firstMarkerIndex !== -1 &&
        lines[firstMarkerIndex + 1] !== 'Write a custom description here.'
    ) {
        return lines.slice(firstMarkerIndex + 1, secondMarkerIndex).join('\n');
    }

    if (secondMarkerIndex !== -1) {
        const thirdMarkerIndex = lines.findIndex(
            (line) => line === thirdMarker
        );

        if (thirdMarkerIndex !== -1) {
            return lines
                .slice(secondMarkerIndex + 1, thirdMarkerIndex)
                .join('\n');
        } else {
            return lines.slice(secondMarkerIndex + 1).join('\n');
        }
    }

    input = input.replace(firstMarker, '');
    input = input.replace(secondMarker, '');
    input = input.replace(thirdMarker, '');

    return input;
}
