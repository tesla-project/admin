/*
 * TeSLA Admin
 * Copyright (C) 2019 Universitat Oberta de Catalunya
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

(function($) {
  $.extend($.summernote.lang, {
    'hu-HU': {
      font: {
        bold: 'Félkövér',
        italic: 'Dőlt',
        underline: 'Aláhúzott',
        clear: 'Formázás törlése',
        height: 'Sorköz',
        name: 'Betűtípus',
        strikethrough: 'Áthúzott',
        subscript: 'Subscript',
        superscript: 'Superscript',
        size: 'Betűméret'
      },
      image: {
        image: 'Kép',
        insert: 'Kép beszúrása',
        resizeFull: 'Átméretezés teljes méretre',
        resizeHalf: 'Átméretezés felére',
        resizeQuarter: 'Átméretezés negyedére',
        floatLeft: 'Igazítás balra',
        floatRight: 'Igazítás jobbra',
        floatNone: 'Igazítás törlése',
        shapeRounded: 'Shape: Rounded',
        shapeCircle: 'Shape: Circle',
        shapeThumbnail: 'Shape: Thumbnail',
        shapeNone: 'Shape: None',
        dragImageHere: 'Ide húzhat képet vagy szöveget',
        dropImage: 'Engedje el a képet vagy szöveget',
        selectFromFiles: 'Fájlok kiválasztása',
        maximumFileSize: 'Maximum file size',
        maximumFileSizeError: 'Maximum file size exceeded.',
        url: 'Kép URL címe',
        remove: 'Kép törlése',
        original: 'Original'
      },
      video: {
        video: 'Videó',
        videoLink: 'Videó hivatkozás',
        insert: 'Videó beszúrása',
        url: 'Videó URL címe',
        providers: '(YouTube, Vimeo, Vine, Instagram, DailyMotion vagy Youku)'
      },
      link: {
        link: 'Hivatkozás',
        insert: 'Hivatkozás beszúrása',
        unlink: 'Hivatkozás megszüntetése',
        edit: 'Szerkesztés',
        textToDisplay: 'Megjelenítendő szöveg',
        url: 'Milyen URL címre hivatkozzon?',
        openInNewWindow: 'Megnyitás új ablakban'
      },
      table: {
        table: 'Táblázat',
        addRowAbove: 'Add row above',
        addRowBelow: 'Add row below',
        addColLeft: 'Add column left',
        addColRight: 'Add column right',
        delRow: 'Delete row',
        delCol: 'Delete column',
        delTable: 'Delete table'
      },
      hr: {
        insert: 'Elválasztó vonal beszúrása'
      },
      style: {
        style: 'Stílus',
        p: 'Normál',
        blockquote: 'Idézet',
        pre: 'Kód',
        h1: 'Fejléc 1',
        h2: 'Fejléc 2',
        h3: 'Fejléc 3',
        h4: 'Fejléc 4',
        h5: 'Fejléc 5',
        h6: 'Fejléc 6'
      },
      lists: {
        unordered: 'Listajeles lista',
        ordered: 'Számozott lista'
      },
      options: {
        help: 'Súgó',
        fullscreen: 'Teljes képernyő',
        codeview: 'Kód nézet'
      },
      paragraph: {
        paragraph: 'Bekezdés',
        outdent: 'Behúzás csökkentése',
        indent: 'Behúzás növelése',
        left: 'Igazítás balra',
        center: 'Igazítás középre',
        right: 'Igazítás jobbra',
        justify: 'Sorkizárt'
      },
      color: {
        recent: 'Jelenlegi szín',
        more: 'További színek',
        background: 'Háttérszín',
        foreground: 'Betűszín',
        transparent: 'Átlátszó',
        setTransparent: 'Átlászóság beállítása',
        reset: 'Visszaállítás',
        resetToDefault: 'Alaphelyzetbe állítás'
      },
      shortcut: {
        shortcuts: 'Gyorsbillentyű',
        close: 'Bezárás',
        textFormatting: 'Szöveg formázása',
        action: 'Művelet',
        paragraphFormatting: 'Bekezdés formázása',
        documentStyle: 'Dokumentumstílus',
        extraKeys: 'Extra keys'
      },
      help: {
        'insertParagraph': 'Új bekezdés',
        'undo': 'Visszavonás',
        'redo': 'Újra',
        'tab': 'Behúzás növelése',
        'untab': 'Behúzás csökkentése',
        'bold': 'Félkövérre állítás',
        'italic': 'Dőltre állítás',
        'underline': 'Aláhúzás',
        'strikethrough': 'Áthúzás',
        'removeFormat': 'Formázás törlése',
        'justifyLeft': 'Balra igazítás',
        'justifyCenter': 'Középre igazítás',
        'justifyRight': 'Jobbra igazítás',
        'justifyFull': 'Sorkizárt',
        'insertUnorderedList': 'Számozatlan lista be/ki',
        'insertOrderedList': 'Számozott lista be/ki',
        'outdent': 'Jelenlegi bekezdés behúzásának megszüntetése',
        'indent': 'Jelenlegi bekezdés behúzása',
        'formatPara': 'Blokk formázása bekezdésként (P tag)',
        'formatH1': 'Blokk formázása, mint Fejléc 1',
        'formatH2': 'Blokk formázása, mint Fejléc 2',
        'formatH3': 'Blokk formázása, mint Fejléc 3',
        'formatH4': 'Blokk formázása, mint Fejléc 4',
        'formatH5': 'Blokk formázása, mint Fejléc 5',
        'formatH6': 'Blokk formázása, mint Fejléc 6',
        'insertHorizontalRule': 'Vízszintes vonal beszúrása',
        'linkDialog.show': 'Link párbeszédablak megjelenítése'
      },
      history: {
        undo: 'Visszavonás',
        redo: 'Újra'
      },
      specialChar: {
        specialChar: 'SPECIAL CHARACTERS',
        select: 'Select Special characters'
      }
    }
  });
})(jQuery);
