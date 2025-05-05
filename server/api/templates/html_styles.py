FIO_STYLE = f"""<style>
        @import url('https://fonts.cdnfonts.com/css/roboto');

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, "Helvetica Neue", Helvetica, sans-serif;
            margin: 0;
            padding: 0;
            background: #e7e7e7;
            overflow-x: hidden;
        }}

        .flex {{
            display: flex;
        }}

        .flex-wrap {{
            flex-wrap: wrap;
        }}

        .items-center {{
            align-items: center;
        }}

        .tab-head {{
            position: relative;
            background: white;
            padding: 12px 12px 0px 18px;
            box-shadow: 0 2.5px 4px rgb(184, 183, 183);
            font-size: 16px;

            padding: 7px 20px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .group-block {{
            flex: 1;
            max-width: 700px;
            min-width: 700px;
            width: 100%;
        }}
        .leak {{
            white-space: nowrap;
            height: 30px;
            display: flex;
            align-items: center;
            padding: 0 12px 0 10px;
            line-height: 1;
            background: white;
            border-radius: 5px;
            overflow: auto;
        }}
        
        @media (max-width: 640px) {{
            .tab-head {{
                padding: 7px 8px 0;
                align-items: center;
            }}

            .tab-head .tabs {{
                justify-content: center;
            }}
        }}

        .tab-head .flex div {{
            font-size: 1em !important;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination) {{
            position: relative;
            padding: .625em .5em;
            margin-right: .8125em;
            cursor: pointer;
            background: white;
            user-select: none;
            color: #747474;
            transition: color .15s;
            /*margin-top: .5em;*/
            margin-top: 4px;
            border-bottom: 2px solid transparent;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination):hover,
        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed;
        }}

        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed !important;
        }}

        .tab-count {{
            position: absolute;
            top: -2px;
            right: -4px;
            display: flex;
            align-items: center;
            padding: 0 3px;
            border-radius: 3px;
            height: 16px;
            font-size: 11px;
            /* 12px */
            background: #4400ed;
            color: white;
        }}

        .content {{
            padding: 15px 7.5px 0;
        }}

        .content>div.selected {{
            display: flex;
            flex-wrap: wrap;
            /*padding: 0 2.5px;*/
        }}

        .content>div:not(.content > .selected) {{
            display: none;
        }}

        .item-container {{
            /*min-width: 375px;*/
            width: 50%;
            padding: 0 7.5px;
            margin-bottom: 15px;
        }}

        @media (max-width: 1025px) {{
            .item-container {{
                width: 100%;
            }}
        }}

        .filter-search-arbitrary {{
            margin-left: 7.5px;
        }}

        @media (max-width: 570px) {{
            .item-container {{
                padding: 0 1.5px;
            }}

            .filter-search-arbitrary {{
                margin-left: 1.5px;
            }}
        }}

        .item {{
            background: white;
            padding: 12px 15px;
            border-radius: 4px;
            box-shadow: 0 0 4px #7f7f7f;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}

        .mt-auto {{
            margin-top: auto;
        }}

        .key-word {{
            background: #e0ec90;
            padding: 0 4px;
            border-radius: 4px;
        }}

        .item-title {{
            font-size: 17px;
            font-weight: 600;


            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;

            text-decoration: none;
            color: #333;
        }}

        .item-title:hover {{
            text-decoration: underline;
        }}

        .item-content {{
            font-size: 13px;
            margin-top: 6px;
            margin-bottom: 0px;

            text-align: justify;
            max-height: 80px;
            line-height: 20px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            margin-bottom: auto;
        }}

        .item-more {{
            margin-left: auto;
            font-size: 14px;
            border: 1px solid #000;

            border: 1px solid #e7eaec;
            font-size: 15px;
            height: 29px;
            padding: 0 8px;
            border-radius: 3px;
            transition: .25s;

            display: flex;
            align-items: center;

            text-decoration: none;
            color: #333;
        }}

        .item-more:hover {{
            background: #e7eaec70;
            text-decoration: underline;
        }}

        .item-more svg {{
            width: 13px;
            margin-left: 7px;
        }}

        .item-param {{
            font-size: 13px;
            display: flex;
            /*white-space: nowrap;*/
            font-weight: 600;
            position: relative;
        }}

        .item-info>a+span,
        .item-info>a {{
            white-space: nowrap;
            padding-top: 4px;
        }}

        @media (max-width: 425px) {{
            .item-info {{
                flex-wrap: wrap-reverse;
            }}

            .item-keywords {{
                width: 100%;
                margin-bottom: 3px;
            }}

            .item-info>a+span {{
                margin-left: auto !important;
            }}
        }}

        .query-content {{
            position: relative;
            overflow-x: clip;
            display: flex;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            text-align: justify;
            color: white;
        }}

        .query {{
            color: white;
            background: #9300FF;
            font-size: 11px;
            border-radius: 3px;
            padding: 0px 4px 1px 4px;
            /*padding: 0px 1px 1px 6px;*/
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            right: 0;
            font-size: 11px;
            background: #404f5d;
            color: #fff;
            padding: 3px 5px;
            border-radius: 6px;
            transition: .15s;
            /* display: none; */
            opacity: 0;
        }}

        .prompt::after {{
            content: "▶";
            position: absolute;
            top: 100%;
            left: 10px;
            color: #404f5d;
            height: 9px;
            transform: rotate(90deg);
        }}

        .query:hover+.prompt {{
            display: block !important;
            opacity: 1 !important;
        }}

        .param-text {{
            overflow: hidden;
            margin-left: 8px;
            font-size: 12px;
        }}

        .empty-list {{
            color: #8a6d3b;
            background: #fce7c4;
            border: 1px solid #fad292;
            display: flex;
            align-items: center;
            height: 35px;
            padding: 0 10px;
            border-radius: 4px;
            margin: 0 auto 15px;
        }}

        .empty-list svg {{
            height: 18px;
            margin-right: 7px;
            fill: #8a6d3b;
        }}

        .pagination svg {{
            height: 100%;
            display: flex;
            align-items: center;
            margin: 0 3px;
            padding: 6px 0 !important;
            width: 22px;
        }}

        .pagination {{
            margin-left: auto;
            display: flex;
            align-items: center;
            /*position: absolute;
                right: 10px;
                bottom: 10px;*/
            font-size: 13px;
            height: 25px;
            user-select: none;
        }}

        .pagination>div>*,
        .pagination>*:not(.pagination > div) {{
            height: 100%;
            padding: 0 7px;
            display: flex !important;
            align-items: center !important;
            cursor: pointer;
            background: white;
        }}

        .h-full {{
            height: 100%;
        }}

        .w-full {{
            width: 100%;
        }}

        .w-half {{
            width: 50%;
        }}

        .pagination>*:first-child {{
            border-radius: 4px 0 0 4px;
        }}

        .pagination>*:last-child {{
            border-radius: 0 4px 4px 0;
        }}

        .pagination>div>* {{
            border-bottom: 1px solid transparent;

        }}

        .pagination>div>*.selected,
        .pagination>div>*:hover {{
            border-bottom: 1px solid #3b5998;
            color: #3b5998;
            font-weight: 600;
        }}

        .pagination>.hovered-angle>svg:hover {{
            background: #3b5998;
            fill: white;
        }}

        .pagination div span {{
            display: flex;
            align-items: center;
        }}

        h2 {{
            font-size: 22px;
        }}

        .object-full_name {{
            font-size: 21px;
            margin-top: 0;
            margin-bottom: 0;
            margin-right: 10px;
            white-space: nowrap;
        }}

        @media (max-width: 710px) {{
            .tab-head>.tabs:not(.tab-head .pagination) {{
                margin: 0 -5px;
                font-size: 15px;
            }}
        }}

        @media (max-width: 500px) {{
            .item-container {{
                margin-bottom: 12px;
            }}

            .item {{
                padding: 8px 11px;
            }}

            .item-title {{
                font-size: 14px;
            }}

            .item-more {{
                font-size: 13px;
                height: 25px;
            }}

            .item-more svg {{
                width: 11px;
                margin-left: 7px;
            }}

            .item-content {{
                font-size: 11px;
                margin-top: 5px;
                margin-bottom: auto;
                line-height: 17px;
            }}

            .item-param {{
                font-size: 11px;
                line-height: 14px;
            }}
        }}

        .filter-search-arbitrary {{
            padding: 15px 7.5px 0;
            width: 50%;
        }}

        .filter-search-arbitrary .input {{
            position: relative;
            display: flex;
            box-shadow: 0 0 4px #7f7f7f;
            max-width: 450px;
            margin: auto;
        }}

        .filter-search-arbitrary .input>input {{
            width: 100%;
            height: 28px;
            padding-left: 7px;
            border-radius: 4px;
            border: none;
            outline: none;
        }}

        .filter-search-arbitrary .input svg {{
            position: absolute;
            right: 7px;
            top: 0;
            bottom: 0;
            width: 14px;
            display: flex;
            align-items: center;
            height: 100%;
            fill: #706f6f;
            cursor: pointer;
            transition: .15s;
        }}

        .filter-search-arbitrary .input svg:hover {{
            fill: black;
        }}

        .filter-search-arbitrary .input.selected svg {{
            transform: rotateX(180deg);
        }}

        .scrollbar::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .scrollbar::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .scrollbar::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 5px;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 0 4px #7f7f7f;
        }}

        .arbitrary-keys>div:first-child {{
            border-radius: 4px;
            min-height: 50px;
            max-height: 270px;
            overflow-y: scroll;
            overflow-x: hidden;
            background: white;
            padding: 8px 10px;
            font-size: 14px;
            position: relative;
            z-index: 5;
        }}

        .arbitrary-keys:not(.arbitrary-keys.show) {{
            display: none;
        }}

        .arbitrary-key {{
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }}

        .arbitrary-key span {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .arbitrary-key:not(.arbitrary-key:last-child) {{
            margin-bottom: 8px;
        }}

        .arbitrary-key input {{
            margin: 2px 5px 0 0;
            height: 14.5px !important;
            width: 14.5px !important;
            min-width: 14.5px !important;
            line-height: 1 !important;
            accent-color: #9300FF;
        }}

        .hovered-angle svg {{
            transition: .15s;
        }}

        svg.first-page,
        svg.last-page {{
            margin: 0;
            padding: 5.65px 0 !important;
            width: 22px;
        }}

        .first-page {{
            margin-left: 22px !important;
        }}

        .last-page {{
            margin-right: 22px !important;
        }}

        .hovered-angle {{
            height: 100%;
        }}

        .pagination {{
            border-radius: 4px;
            overflow: hidden;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page,
        .hovered-angle:not(.hovered-angle:hover) svg.last-page {{
            width: 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg:not(svg.last-page) {{
            border-radius: 0 4px 4px 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page+svg {{
            border-radius: 4px 0 0 4px;
        }}

        .hovered-angle:hover svg.first-page,
        .hovered-angle:hover svg.last-page {{
            margin: 0 !important;
        }}

        .pagination-container {{
            padding: 15px 7.5px 0;
            margin: auto;
        }}

        @media (max-width: 670px) {{

            .hovered-angle:hover svg:not(svg.last-page) {{
                border-radius: 0 4px 4px 0 !important;
            }}

            .hovered-angle:hover svg.first-page+svg {{
                border-radius: 4px 0 0 4px !important;
            }}

            .filter-search-arbitrary {{
                width: 100%;
            }}

            .wrap-reverse-container {{
                flex-wrap: wrap-reverse;
            }}

            svg.first-page,
            svg.last-page {{
                display: none !important;
            }}

            .pagination .flex.h-full {{
                max-width: 250px;
                overflow-y: hidden;
                overflow-x: scroll;
                margin-bottom: 0px;
                min-height: 34px !important;
            }}

            .pagination .flex.h-full>* {{
                height: 26px !important;
            }}

            .pagination {{
                height: 33px;
                margin-bottom: -8px;
            }}

            .pagination .hovered-angle {{
                padding-bottom: 8px;
            }}
        }}

        .filter-btns {{
            background: white;
            position: relative;
            z-index: 1;
            border-top: 1px solid #ccc;
            font-size: 15px;
            display: flex;
        }}

        .filter-btns span {{
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-around;
            height: 38px;
            cursor: pointer;
            transition: .15s;
            padding-bottom: 1px;
        }}

        .filter-btns span:first-child {{
            border-right: 1px solid #ccc;
        }}

        .filter-btns span:hover {{
            color: white;
            background: #9300FF;
        }}

        .filter-info {{
            position: absolute !important;
            top: unset !important;
            bottom: 38px !important;
            right: 0 !important;
            margin: 5px;
            z-index: 15;
            width: 18.5px !important;
            height: 18.5px !important;
        }}

        .filter-info svg {{
            width: 18.5px !important;
            height: 18.5px !important;
            fill: rgba(131, 131, 131, 0.58) !important;
            transform: rotateX(0deg) !important;
        }}

        .filter-info svg:hover {{
            fill: #838383 !important;
        }}

        .filter-info .filter-info_prompt {{
            position: absolute;
            bottom: calc(100% + 9px);
            right: 0;
            background: #838383;
            color: white;
            font-size: 11px;
            white-space: nowrap;
            padding: 3px 5px;
            border-radius: 4px;
            transition: .15s;
        }}

        .filter-info_prompt::after {{
            content: "▶";
            position: absolute;
            top: calc(100% - 1.5px);
            right: 8.5px;
            color: #838383;
            height: 3px;
            transform: rotate(90deg);
        }}

        .filter-info svg:not(.filter-info svg:hover)+.filter-info_prompt {{
            opacity: 0;
            pointer-events: none;
        }}

        .similars-range {{
            max-width: 300px;
            width: 100%;
            /*max-height: 25px;*/
            position: relative;

            margin: 15px 7.5px 0;
            padding-top: 11.5px;
            height: 25px;
            background: white;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0, 0, 0, .15);
            margin-left: auto !important;
            margin-right: auto !important;
        }}

        .similars-range input {{
            position: absolute;
            top: 0;
            left: 0;
        }}

        /* Range */

        [slider] {{
            position: relative;
            height: 3px;
            border-radius: 10px;
            text-align: left;
            display: flex;
            align-items: center;
        }}

        [slider]>div {{
            position: absolute;
            left: 13px;
            right: 15px;
            height: 3px;
        }}

        [slider]>div>[inverse-left] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[inverse-right] {{
            position: absolute;
            right: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[range] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 14px;
            background-color: #4169e1;
        }}

        [slider]>div>[thumb] {{
            position: absolute;
            top: -5px;
            z-index: 2;
            height: 12px;
            width: 12px;
            text-align: left;
            margin-left: -7px;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
            background-color: #FFF;
            border-radius: 3px;
            outline: none;
        }}

        [slider]>input[type=range] {{
            position: absolute;
            pointer-events: none;
            -webkit-appearance: none;
            z-index: 3;
            height: 3px;
            top: -2px;
            width: 100%;
            -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
            filter: alpha(opacity=0);
            -moz-opacity: 0;
            -khtml-opacity: 0;
            opacity: 0;
        }}

        div[slider]>input[type=range]::-ms-track {{
            -webkit-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]::-moz-range-track {{
            -moz-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]:focus::-webkit-slider-runnable-track {{
            background: transparent;
            border: transparent;
        }}

        div[slider]>input[type=range]:focus {{
            outline: none;
        }}

        div[slider]>input[type=range]::-ms-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-moz-range-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-webkit-slider-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
            -webkit-appearance: none;
        }}

        div[slider]>input[type=range]::-ms-fill-lower {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-fill-upper {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-tooltip {{
            display: none;
        }}

        [slider]>div>[sign] {{
            font-size: 15px;
            opacity: 0;
            position: absolute;
            margin-left: -13px;
            top: -2.4375em;
            z-index: 3;
            background-color: #4169e1;
            color: #fff;
            width: 1.75em;
            height: 1.75em;
            border-radius: 1.75em;
            -webkit-border-radius: 1.75em;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            text-align: center;
        }}

        [slider]>div>[sign]:after {{
            position: absolute;
            content: '';
            left: 0;
            border-radius: 1em;
            top: calc(1.1875em + 1px);
            border-left: 0.875em solid transparent;
            border-right: 0.875em solid transparent;
            border-top-width: 1em;
            border-top-style: solid;
            border-top-color: #4169e1;
        }}

        [slider]>div>[sign]>span {{
            font-size: 10px;
            font-weight: 700;
            line-height: 28px;
        }}

        [slider]:hover>div>[sign] {{
            opacity: 1;
        }}

        .clone {{
            width: 16px;
            height: 16px;
            fill: #4169e1;
        }}

        .seen_link {{
            opacity: 0.8;
        }}

        .seen_link .item {{
            box-shadow: none;
            background: #c4d9ce;
        }}

        .filter-count {{
            margin-left: auto;
            background: #9300FF;
            color: white;
            padding: 0 4px;
            border-radius: 4px;
            font-size: 13px;
            white-space: nowrap;
        }}

        /* ------------------------------------ */

        .checkmark__circle {{
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 5;
            stroke-miterlimit: 10;
            stroke: #4400ed;
            fill: none;
            animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
        }}

        .checkmark {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: block;
            stroke-width: 6.5;
            stroke: #fff;
            stroke-miterlimit: 10;
            box-shadow: inset 0px 0px 0px #4400ed;
            animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;

            margin-right: 5px;
            position: absolute;
            top: -5px;
            left: -5px;
        }}

        .checkmark.unseen {{
            top: 6px;
            left: 6px;
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }}

        .checkmark.unseen.seen_scale {{
            animation: fill .4s ease-in-out .4s forwards, seen_scale .3s ease-in-out .9s both;
        }}

        .checkmark__check {{
            transform-origin: 50% 50%;
            stroke-dasharray: 48;
            stroke-dashoffset: 48;
            animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
        }}

        @keyframes stroke {{
            100% {{
                stroke-dashoffset: 0;
            }}
        }}

        @keyframes scale {{

            0%,
            100% {{
                transform: none;
            }}

            50% {{
                transform: scale3d(1.1, 1.1, 1);
            }}
        }}

        @keyframes seen_scale {{
            20% {{
                transform: scale3d(1.1, 1.1, 1);
            }}

            99% {{
                transform: scale3d(0, 0, 0);
            }}

            99% {{
                display: none;
            }}
        }}

        @keyframes fill {{
            100% {{
                box-shadow: inset 0px 0px 0px 20px #4400ed;
            }}
        }}

        .documents,
        .socials {{
            display: flex;
            align-items: center;
            padding: 0 9px;
            background: white;
            border-radius: 5px;
            height: 40px;
            margin-top: -2.5px;
        }}

        .doc_type,
        .social_type {{
            width: 19px;
            height: 18px;
            transition: .25s all;
            color: #bbb;
        }}
        
        .doc_type-info,
        .socials_type-info {{
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 10px;
            margin-bottom: -1px;
            cursor: pointer;
        }}

        .doc_type-info:not(.doc_type-info:last-child),
        .socials_type-info:not(.socials_type-info:last-child) {{
            margin-right: 11px;
        }}

        .doc_type {{
            fill: #bbb;
        }}
        .doc_type.pdf.selected,
        .doc_type.pdf:hover {{
            fill: #e10000;
        }}
        .doc_type.word.selected,
        .doc_type.word:hover {{
            fill: #0583f3;
        }}
        .doc_type.excel.selected,
        .doc_type.excel:hover {{
            fill: #00ac0f;
        }}
        .doc_type.pptx.selected,
        .doc_type.pptx:hover {{
            fill: #f2b90a;
        }}
        .doc_type.txt.selected,
        .doc_type.txt:hover {{
            fill: #444444;
        }}



        .social_type.vk {{
            fill: #bbb;
        }}

        .social_type.vk.selected,
        .social_type.vk:hover {{
            fill: #4a76a8;
        }}

        .social_type.fb {{
            fill: #bbb;
        }}

        .social_type.fb.selected,
        .social_type.fb:hover {{
            fill: #4267b2;
        }}

        .social_type.insta {{
            fill: #fff;
            border-radius: 6px;
            /* display: flex;
            align-items: center;
            justify-content: center; */
            /* vertical-align: text-bottom; */
            background: #bbb;
            padding: 1px;
        }}

        .social_type.insta.selected,
        .social_type.insta:hover {{
            background: linear-gradient(#a900ff, #ea3701, #ec920b);
        }}

        .social_type.tg {{
            fill: #bbb;
        }}

        .social_type.tg.selected,
        .social_type.tg:hover {{
            fill: #1da1f2;
        }}

        .social_type.ok {{
            fill: #bbb;
        }}

        .social_type.ok.selected,
        .social_type.ok:hover {{
            fill: #ee8208;
        }}
        .max-text-length {{
            font-size: 11px;
            max-width: 600px;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
        }}

        /* Minus-Keywords */

        
        .minus-keyword {{
            display: flex;
            align-items: center;
            padding: 3px 5px 5px 8px;
            font-size: 14px;
            cursor: default;
        }}
        .minus-keyword span {{
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            user-select: none;
        }}
        .minus-keyword svg {{
            padding: 0 2px 0 4px;
            width: 21px;
            height: 13px;
            cursor: pointer;
        }}
        .minus-keyword svg:hover {{
            fill: red;
        }}
        .minus-keyword:hover {{
            background: #f5f4f4;
        }}
        .minus-keywords-modal {{
            position: absolute;
            top: 100%;
            right: 0;
            left: 0;
            max-height: 150px;
            background: white;
            margin-top: 3px;
            border-radius: 3px;
            display: flex;
            flex-direction: column;
            overflow-y: scroll;
            overflow-x: hidden;
            transition: .15s;
        }}
        .minus-keywords-modal.hide-keywords-modal {{
            max-height: 0px;
        }}
        .parent-prompt-hover,
        .parent-prompt {{
            position: relative !important;
        }}
        .parent-prompt input:not(.parent-prompt input:focus) + .prompt {{
            opacity: 0;
            display: none;
        }}
        .parent-prompt-hover:not(.parent-prompt-hover:hover) .prompt {{
            opacity: 0;
            display: none;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            left: 0;
            font-size: 13px;
            background: #404f5d;
            color: #fff;
            padding: 6px;
            border-radius: 6px;
            transition: .15s;
            opacity: 1;
        }}


</style>"""









COMPANY_STYLE = f"""
<style>
        @import url('https://fonts.cdnfonts.com/css/roboto');

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, "Helvetica Neue", Helvetica, sans-serif;
            margin: 0;
            padding: 0;
            background: #e7e7e7;
            overflow-x: hidden;
        }}

        .flex {{
            display: flex;
        }}

        .flex-wrap {{
            flex-wrap: wrap;
        }}

        .items-center {{
            align-items: center;
        }}

        .tab-head {{
            position: relative;
            background: white;
            padding: 12px 12px 0px 18px;
            box-shadow: 0 2.5px 4px rgb(184, 183, 183);
            font-size: 16px;

            padding: 7px 20px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        @media (max-width: 640px) {{
            .tab-head {{
                padding: 7px 8px 0;
                align-items: center;
            }}

            .tab-head .tabs {{
                justify-content: center;
            }}
        }}

        .tab-head .flex div {{
            font-size: 1em !important;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination) {{
            position: relative;
            padding: .625em .5em;
            margin-right: .8125em;
            cursor: pointer;
            background: white;
            user-select: none;
            color: #747474;
            transition: color .15s;
            /*margin-top: .5em;*/
            margin-top: 4px;
            border-bottom: 2px solid transparent;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination):hover,
        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed;
        }}

        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed !important;
        }}

        .tab-count {{
            position: absolute;
            top: -2px;
            right: -4px;
            display: flex;
            align-items: center;
            padding: 0 3px;
            border-radius: 3px;
            height: 16px;
            font-size: 11px;
            /* 12px */
            background: #4400ed;
            color: white;
        }}

        .content {{
            padding: 15px 7.5px 0;
        }}

        .content>div.selected {{
            display: flex;
            flex-wrap: wrap;
            /*padding: 0 2.5px;*/
        }}

        .content>div:not(.content > .selected) {{
            display: none;
        }}

        .item-container {{
            /*min-width: 375px;*/
            width: 50%;
            padding: 0 7.5px;
            margin-bottom: 15px;
        }}

        @media (max-width: 1025px) {{
            .item-container {{
                width: 100%;
            }}
        }}

        .filter-search-arbitrary {{
            margin-left: 7.5px;
        }}

        @media (max-width: 570px) {{
            .item-container {{
                padding: 0 1.5px;
            }}

            .filter-search-arbitrary {{
                margin-left: 1.5px;
            }}
        }}

        .item {{
            background: white;
            padding: 12px 15px;
            border-radius: 4px;
            box-shadow: 0 0 4px #7f7f7f;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}

        .mt-auto {{
            margin-top: auto;
        }}

        .key-word {{
            background: #e0ec90;
            padding: 0 4px;
            border-radius: 4px;
        }}

        .item-title {{
            font-size: 17px;
            font-weight: 600;


            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;

            text-decoration: none;
            color: #333;
        }}

        .item-title:hover {{
            text-decoration: underline;
        }}

        .item-content {{
            font-size: 13px;
            margin-top: 6px;
            margin-bottom: 0px;

            text-align: justify;
            max-height: 80px;
            line-height: 20px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            margin-bottom: auto;
        }}

        .item-more {{
            margin-left: auto;
            font-size: 14px;
            border: 1px solid #000;

            border: 1px solid #e7eaec;
            font-size: 15px;
            height: 29px;
            padding: 0 8px;
            border-radius: 3px;
            transition: .25s;

            display: flex;
            align-items: center;

            text-decoration: none;
            color: #333;
        }}

        .item-more:hover {{
            background: #e7eaec70;
            text-decoration: underline;
        }}

        .item-more svg {{
            width: 13px;
            margin-left: 7px;
        }}

        .item-param {{
            font-size: 13px;
            display: flex;
            /*white-space: nowrap;*/
            font-weight: 600;
            position: relative;
        }}

        .item-info>a+span,
        .item-info>a {{
            white-space: nowrap;
            padding-top: 4px;
        }}

        @media (max-width: 425px) {{
            .item-info {{
                flex-wrap: wrap-reverse;
            }}

            .item-keywords {{
                width: 100%;
                margin-bottom: 3px;
            }}

            .item-info>a+span {{
                margin-left: auto !important;
            }}
        }}

        .query-content {{
            position: relative;
            overflow-x: clip;
            display: flex;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            text-align: justify;
            color: white;
        }}

        .query {{
            color: white;
            background: #9300FF;
            font-size: 11px;
            border-radius: 3px;
            padding: 0px 4px 1px 4px;
            /*padding: 0px 1px 1px 6px;*/
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            right: 0;
            font-size: 11px;
            background: #404f5d;
            color: #fff;
            padding: 3px 5px;
            border-radius: 6px;
            transition: .15s;
            display: none;
            opacity: 0;
        }}

        .prompt::after {{
            content: "▶";
            position: absolute;
            top: 100%;
            left: 10px;
            color: #404f5d;
            height: 9px;
            transform: rotate(90deg);
        }}

        .query:hover+.prompt {{
            display: block !important;
            opacity: 1 !important;
        }}

        .param-text {{
            overflow: hidden;
            margin-left: 8px;
            font-size: 12px;
        }}

        .empty-list {{
            color: #8a6d3b;
            background: #fce7c4;
            border: 1px solid #fad292;
            display: flex;
            align-items: center;
            height: 35px;
            padding: 0 10px;
            border-radius: 4px;
            margin: 0 auto 15px;
        }}

        .empty-list svg {{
            height: 18px;
            margin-right: 7px;
            fill: #8a6d3b;
        }}

        .pagination svg {{
            height: 100%;
            display: flex;
            align-items: center;
            margin: 0 3px;
            padding: 6px 0 !important;
            width: 22px;
        }}

        .pagination {{
            margin-left: auto;
            display: flex;
            align-items: center;
            /*position: absolute;
                right: 10px;
                bottom: 10px;*/
            font-size: 13px;
            height: 25px;
            user-select: none;
        }}

        .pagination>div>*,
        .pagination>*:not(.pagination > div) {{
            height: 100%;
            padding: 0 7px;
            display: flex !important;
            align-items: center !important;
            cursor: pointer;
            background: white;
        }}

        .h-full {{
            height: 100%;
        }}

        .w-full {{
            width: 100%;
        }}

        .w-half {{
            width: 50%;
        }}

        .pagination>*:first-child {{
            border-radius: 4px 0 0 4px;
        }}

        .pagination>*:last-child {{
            border-radius: 0 4px 4px 0;
        }}

        .pagination>div>* {{
            border-bottom: 1px solid transparent;

        }}

        .pagination>div>*.selected,
        .pagination>div>*:hover {{
            border-bottom: 1px solid #3b5998;
            color: #3b5998;
            font-weight: 600;
        }}

        .pagination>.hovered-angle>svg:hover {{
            background: #3b5998;
            fill: white;
        }}

        .pagination div span {{
            display: flex;
            align-items: center;
        }}

        h2 {{
            font-size: 22px;
        }}

        .object-full_name {{
            font-size: 21px;
            margin-top: 0;
            margin-bottom: 0;
            margin-right: 10px;
            white-space: nowrap;
        }}

        @media (max-width: 710px) {{
            .tab-head>.tabs:not(.tab-head .pagination) {{
                margin: 0 -5px;
                font-size: 15px;
            }}
        }}

        @media (max-width: 500px) {{
            .item-container {{
                margin-bottom: 12px;
            }}

            .item {{
                padding: 8px 11px;
            }}

            .item-title {{
                font-size: 14px;
            }}

            .item-more {{
                font-size: 13px;
                height: 25px;
            }}

            .item-more svg {{
                width: 11px;
                margin-left: 7px;
            }}

            .item-content {{
                font-size: 11px;
                margin-top: 5px;
                margin-bottom: auto;
                line-height: 17px;
            }}

            .item-param {{
                font-size: 11px;
                line-height: 14px;
            }}
        }}

        .filter-search-arbitrary {{
            padding: 15px 7.5px 0;
            width: 50%;
        }}

        .filter-search-arbitrary .input {{
            position: relative;
            display: flex;
            box-shadow: 0 0 4px #7f7f7f;
            max-width: 450px;
            margin: auto;
        }}

        .filter-search-arbitrary .input>input {{
            width: 100%;
            height: 28px;
            padding-left: 7px;
            border-radius: 4px;
            border: none;
            outline: none;
        }}

        .filter-search-arbitrary .input svg {{
            position: absolute;
            right: 7px;
            top: 0;
            bottom: 0;
            width: 14px;
            display: flex;
            align-items: center;
            height: 100%;
            fill: #706f6f;
            cursor: pointer;
            transition: .15s;
        }}

        .filter-search-arbitrary .input svg:hover {{
            fill: black;
        }}

        .filter-search-arbitrary .input.selected svg {{
            transform: rotateX(180deg);
        }}

        .scrollbar::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .scrollbar::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .scrollbar::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 5px;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 0 4px #7f7f7f;
        }}

        .arbitrary-keys>div:first-child {{
            border-radius: 4px;
            min-height: 50px;
            max-height: 270px;
            overflow-y: scroll;
            overflow-x: hidden;
            background: white;
            padding: 8px 10px;
            font-size: 14px;
            position: relative;
            z-index: 5;
        }}

        .arbitrary-keys:not(.arbitrary-keys.show) {{
            display: none;
        }}

        .arbitrary-key {{
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }}

        .arbitrary-key span {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .arbitrary-key:not(.arbitrary-key:last-child) {{
            margin-bottom: 8px;
        }}

        .arbitrary-key input {{
            margin: 2px 5px 0 0;
            height: 14.5px !important;
            width: 14.5px !important;
            min-width: 14.5px !important;
            line-height: 1 !important;
            accent-color: #9300FF;
        }}

        .hovered-angle svg {{
            transition: .15s;
        }}

        svg.first-page,
        svg.last-page {{
            margin: 0;
            padding: 5.65px 0 !important;
            width: 22px;
        }}

        .first-page {{
            margin-left: 22px !important;
        }}

        .last-page {{
            margin-right: 22px !important;
        }}

        .hovered-angle {{
            height: 100%;
        }}

        .pagination {{
            border-radius: 4px;
            overflow: hidden;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page,
        .hovered-angle:not(.hovered-angle:hover) svg.last-page {{
            width: 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg:not(svg.last-page) {{
            border-radius: 0 4px 4px 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page+svg {{
            border-radius: 4px 0 0 4px;
        }}

        .hovered-angle:hover svg.first-page,
        .hovered-angle:hover svg.last-page {{
            margin: 0 !important;
        }}

        .pagination-container {{
            padding: 15px 7.5px 0;
            margin: auto;
        }}

        @media (max-width: 670px) {{

            .hovered-angle:hover svg:not(svg.last-page) {{
                border-radius: 0 4px 4px 0 !important;
            }}

            .hovered-angle:hover svg.first-page+svg {{
                border-radius: 4px 0 0 4px !important;
            }}

            .filter-search-arbitrary {{
                width: 100%;
            }}

            .wrap-reverse-container {{
                flex-wrap: wrap-reverse;
            }}

            svg.first-page,
            svg.last-page {{
                display: none !important;
            }}

            .pagination .flex.h-full {{
                max-width: 250px;
                overflow-y: hidden;
                overflow-x: scroll;
                margin-bottom: 0px;
                min-height: 34px !important;
            }}

            .pagination .flex.h-full>* {{
                height: 26px !important;
            }}

            .pagination {{
                height: 33px;
                margin-bottom: -8px;
            }}

            .pagination .hovered-angle {{
                padding-bottom: 8px;
            }}
        }}

        .filter-btns {{
            background: white;
            position: relative;
            z-index: 1;
            border-top: 1px solid #ccc;
            font-size: 15px;
            display: flex;
        }}

        .filter-btns span {{
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-around;
            height: 38px;
            cursor: pointer;
            transition: .15s;
            padding-bottom: 1px;
        }}

        .filter-btns span:first-child {{
            border-right: 1px solid #ccc;
        }}

        .filter-btns span:hover {{
            color: white;
            background: #9300FF;
        }}

        .filter-info {{
            position: absolute !important;
            top: unset !important;
            bottom: 38px !important;
            right: 0 !important;
            margin: 5px;
            z-index: 15;
            width: 18.5px !important;
            height: 18.5px !important;
        }}

        .filter-info svg {{
            width: 18.5px !important;
            height: 18.5px !important;
            fill: rgba(131, 131, 131, 0.58) !important;
            transform: rotateX(0deg) !important;
        }}

        .filter-info svg:hover {{
            fill: #838383 !important;
        }}

        .filter-info .filter-info_prompt {{
            position: absolute;
            bottom: calc(100% + 9px);
            right: 0;
            background: #838383;
            color: white;
            font-size: 11px;
            white-space: nowrap;
            padding: 3px 5px;
            border-radius: 4px;
            transition: .15s;
        }}

        .filter-info_prompt::after {{
            content: "▶";
            position: absolute;
            top: calc(100% - 1.5px);
            right: 8.5px;
            color: #838383;
            height: 3px;
            transform: rotate(90deg);
        }}

        .filter-info svg:not(.filter-info svg:hover)+.filter-info_prompt {{
            opacity: 0;
            pointer-events: none;
        }}

        .similars-range {{
            max-width: 300px;
            width: 100%;
            /*max-height: 25px;*/
            position: relative;

            margin: 15px 7.5px 0;
            padding-top: 11.5px;
            height: 25px;
            background: white;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0, 0, 0, .15);
            margin-left: auto !important;
            margin-right: auto !important;
        }}

        .similars-range input {{
            position: absolute;
            top: 0;
            left: 0;
        }}

        /* Range */

        [slider] {{
            position: relative;
            height: 3px;
            border-radius: 10px;
            text-align: left;
            display: flex;
            align-items: center;
        }}

        [slider]>div {{
            position: absolute;
            left: 13px;
            right: 15px;
            height: 3px;
        }}

        [slider]>div>[inverse-left] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[inverse-right] {{
            position: absolute;
            right: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[range] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 14px;
            background-color: #4169e1;
        }}

        [slider]>div>[thumb] {{
            position: absolute;
            top: -5px;
            z-index: 2;
            height: 12px;
            width: 12px;
            text-align: left;
            margin-left: -7px;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
            background-color: #FFF;
            border-radius: 3px;
            outline: none;
        }}

        [slider]>input[type=range] {{
            position: absolute;
            pointer-events: none;
            -webkit-appearance: none;
            z-index: 3;
            height: 3px;
            top: -2px;
            width: 100%;
            -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
            filter: alpha(opacity=0);
            -moz-opacity: 0;
            -khtml-opacity: 0;
            opacity: 0;
        }}

        div[slider]>input[type=range]::-ms-track {{
            -webkit-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]::-moz-range-track {{
            -moz-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]:focus::-webkit-slider-runnable-track {{
            background: transparent;
            border: transparent;
        }}

        div[slider]>input[type=range]:focus {{
            outline: none;
        }}

        div[slider]>input[type=range]::-ms-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-moz-range-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-webkit-slider-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
            -webkit-appearance: none;
        }}

        div[slider]>input[type=range]::-ms-fill-lower {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-fill-upper {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-tooltip {{
            display: none;
        }}

        [slider]>div>[sign] {{
            font-size: 15px;
            opacity: 0;
            position: absolute;
            margin-left: -13px;
            top: -2.4375em;
            z-index: 3;
            background-color: #4169e1;
            color: #fff;
            width: 1.75em;
            height: 1.75em;
            border-radius: 1.75em;
            -webkit-border-radius: 1.75em;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            text-align: center;
        }}

        [slider]>div>[sign]:after {{
            position: absolute;
            content: '';
            left: 0;
            border-radius: 1em;
            top: calc(1.1875em + 1px);
            border-left: 0.875em solid transparent;
            border-right: 0.875em solid transparent;
            border-top-width: 1em;
            border-top-style: solid;
            border-top-color: #4169e1;
        }}

        [slider]>div>[sign]>span {{
            font-size: 10px;
            font-weight: 700;
            line-height: 28px;
        }}

        [slider]:hover>div>[sign] {{
            opacity: 1;
        }}

        .clone {{
            width: 16px;
            height: 16px;
            fill: #4169e1;
        }}

        .seen_link {{
            opacity: 0.8;
        }}

        .seen_link .item {{
            box-shadow: none;
            background: #c4d9ce;
        }}

        .filter-count {{
            margin-left: auto;
            background: #9300FF;
            color: white;
            padding: 0 4px;
            border-radius: 4px;
            font-size: 13px;
            white-space: nowrap;
        }}

        /* ------------------------------------ */

        .checkmark__circle {{
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 5;
            stroke-miterlimit: 10;
            stroke: #4400ed;
            fill: none;
            animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
        }}

        .checkmark {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: block;
            stroke-width: 6.5;
            stroke: #fff;
            stroke-miterlimit: 10;
            box-shadow: inset 0px 0px 0px #4400ed;
            animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;

            margin-right: 5px;
            position: absolute;
            top: -5px;
            left: -5px;
        }}

        .checkmark.unseen {{
            top: 6px;
            left: 6px;
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }}

        .checkmark.unseen.seen_scale {{
            animation: fill .4s ease-in-out .4s forwards, seen_scale .3s ease-in-out .9s both;
        }}

        .checkmark__check {{
            transform-origin: 50% 50%;
            stroke-dasharray: 48;
            stroke-dashoffset: 48;
            animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
        }}

        @keyframes stroke {{
            100% {{
                stroke-dashoffset: 0;
            }}
        }}

        @keyframes scale {{

            0%,
            100% {{
                transform: none;
            }}

            50% {{
                transform: scale3d(1.1, 1.1, 1);
            }}
        }}

        @keyframes seen_scale {{
            20% {{
                transform: scale3d(1.1, 1.1, 1);
            }}

            99% {{
                transform: scale3d(0, 0, 0);
            }}

            99% {{
                display: none;
            }}
        }}

        @keyframes fill {{
            100% {{
                box-shadow: inset 0px 0px 0px 20px #4400ed;
            }}
        }}

        .documents,
        .socials {{
            display: flex;
            align-items: center;
            padding: 0 9px;
            background: white;
            border-radius: 5px;
            height: 40px;
            margin-top: -2.5px;
        }}

        .doc_type,
        .social_type {{
            width: 19px;
            height: 18px;
            transition: .25s all;
            color: #bbb;
        }}
        
        .doc_type-info,
        .socials_type-info {{
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 10px;
            margin-bottom: -1px;
            cursor: pointer;
        }}

        .doc_type-info:not(.doc_type-info:last-child),
        .socials_type-info:not(.socials_type-info:last-child) {{
            margin-right: 11px;
        }}

        .doc_type {{
            fill: #bbb;
        }}
        .doc_type.pdf.selected,
        .doc_type.pdf:hover {{
            fill: #e10000;
        }}
        .doc_type.word.selected,
        .doc_type.word:hover {{
            fill: #0583f3;
        }}
        .doc_type.excel.selected,
        .doc_type.excel:hover {{
            fill: #00ac0f;
        }}
        .doc_type.pptx.selected,
        .doc_type.pptx:hover {{
            fill: #f2b90a;
        }}
        .doc_type.txt.selected,
        .doc_type.txt:hover {{
            fill: #444444;
        }}



        .social_type.vk {{
            fill: #bbb;
        }}

        .social_type.vk.selected,
        .social_type.vk:hover {{
            fill: #4a76a8;
        }}

        .social_type.fb {{
            fill: #bbb;
        }}

        .social_type.fb.selected,
        .social_type.fb:hover {{
            fill: #4267b2;
        }}

        .social_type.insta {{
            fill: #fff;
            border-radius: 6px;
            /* display: flex;
            align-items: center;
            justify-content: center; */
            /* vertical-align: text-bottom; */
            background: #bbb;
            padding: 1px;
        }}

        .social_type.insta.selected,
        .social_type.insta:hover {{
            background: linear-gradient(#a900ff, #ea3701, #ec920b);
        }}

        .social_type.tg {{
            fill: #bbb;
        }}

        .social_type.tg.selected,
        .social_type.tg:hover {{
            fill: #1da1f2;
        }}

        .social_type.ok {{
            fill: #bbb;
        }}

        .social_type.ok.selected,
        .social_type.ok:hover {{
            fill: #ee8208;
        }}
        .max-text-length {{
            font-size: 11px;
            max-width: 600px;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
        }}


        /* Minus-Keywords */
        
        .minus-keyword {{
            display: flex;
            align-items: center;
            padding: 3px 5px 5px 8px;
            font-size: 14px;
            cursor: default;
        }}
        .minus-keyword span {{
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            user-select: none;
        }}
        .minus-keyword svg {{
            padding: 0 2px 0 4px;
            width: 21px;
            height: 13px;
            cursor: pointer;
        }}
        .minus-keyword svg:hover {{
            fill: red;
        }}
        .minus-keyword:hover {{
            background: #f5f4f4;
        }}
        .minus-keywords-modal {{
            position: absolute;
            top: 100%;
            right: 0;
            left: 0;
            max-height: 150px;
            background: white;
            margin-top: 3px;
            border-radius: 3px;
            display: flex;
            flex-direction: column;
            overflow-y: scroll;
            overflow-x: hidden;
            transition: .15s;
        }}
        .minus-keywords-modal.hide-keywords-modal {{
            max-height: 0px;
        }}
        .parent-prompt {{
            position: relative !important;
        }}
        .parent-prompt input:not(.parent-prompt input:focus) + .prompt {{
            opacity: 0;
            display: none;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            left: 0;
            font-size: 13px;
            background: #404f5d;
            color: #fff;
            padding: 6px;
            border-radius: 6px;
            transition: .15s;
            opacity: 1;
        }}
    </style>
"""










NUM_STYLE = f"""<style>
        @import url('https://fonts.cdnfonts.com/css/roboto');

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, "Helvetica Neue", Helvetica, sans-serif;
            margin: 0;
            padding: 0;
            background: #e7e7e7;
            overflow-x: hidden;
        }}

        .flex {{
            display: flex;
        }}
        .flex-col {{
            flex-direction: column;
        }}

        .flex-wrap {{
            flex-wrap: wrap;
        }}

        .items-center {{
            align-items: center;
        }}

        .tab-head {{
            position: relative;
            background: white;
            padding: 12px 12px 0px 18px;
            box-shadow: 0 2.5px 4px rgb(184, 183, 183);
            font-size: 16px;

            padding: 7px 20px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        @media (max-width: 640px) {{
            .tab-head {{
                padding: 7px 8px 0;
                align-items: center;
            }}

            .tab-head .tabs {{
                justify-content: center;
            }}
        }}

        .tab-head .flex div {{
            font-size: 1em !important;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination) {{
            position: relative;
            padding: .625em .5em;
            margin-right: .8125em;
            cursor: pointer;
            background: white;
            user-select: none;
            color: #747474;
            transition: color .15s;
            /*margin-top: .5em;*/
            margin-top: 4px;
            border-bottom: 2px solid transparent;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination):hover,
        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed;
        }}

        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed !important;
        }}

        .tab-count {{
            position: absolute;
            top: -2px;
            right: -4px;
            display: flex;
            align-items: center;
            padding: 0 3px;
            border-radius: 3px;
            height: 16px;
            font-size: 11px;
            /* 12px */
            background: #4400ed;
            color: white;
        }}

        .content {{
            padding: 15px 7.5px 0;
        }}

        .content>div.selected {{
            display: flex;
            flex-wrap: wrap;
            /*padding: 0 2.5px;*/
        }}

        .content>div:not(.content > .selected) {{
            display: none;
        }}

        .item-container {{
            /*min-width: 375px;*/
            width: 50%;
            padding: 0 7.5px;
            margin-bottom: 15px;
        }}

        @media (max-width: 1025px) {{
            .item-container {{
                width: 100%;
            }}
        }}

        .filter-search-arbitrary {{
            margin-left: 7.5px;
        }}

        @media (max-width: 570px) {{
            .item-container {{
                padding: 0 1.5px;
            }}

            .filter-search-arbitrary {{
                margin-left: 1.5px;
            }}
        }}

        .item {{
            background: white;
            padding: 12px 15px;
            border-radius: 4px;
            box-shadow: 0 0 4px #7f7f7f;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}

        .mt-auto {{
            margin-top: auto;
        }}

        .key-word {{
            background: #e0ec90;
            padding: 0 4px;
            border-radius: 4px;
        }}

        .item-title {{
            font-size: 17px;
            font-weight: 600;


            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;

            text-decoration: none;
            color: #333;
        }}

        .item-title:hover {{
            text-decoration: underline;
        }}

        .item-content {{
            font-size: 13px;
            margin-top: 6px;
            margin-bottom: 0px;

            text-align: justify;
            max-height: 80px;
            line-height: 20px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            margin-bottom: auto;
        }}

        .item-more {{
            margin-left: auto;
            font-size: 14px;
            border: 1px solid #000;

            border: 1px solid #e7eaec;
            font-size: 15px;
            height: 29px;
            padding: 0 8px;
            border-radius: 3px;
            transition: .25s;

            display: flex;
            align-items: center;

            text-decoration: none;
            color: #333;
        }}

        .item-more:hover {{
            background: #e7eaec70;
            text-decoration: underline;
        }}

        .item-more svg {{
            width: 13px;
            margin-left: 7px;
        }}

        .item-param {{
            font-size: 13px;
            display: flex;
            /*white-space: nowrap;*/
            font-weight: 600;
            position: relative;
        }}
        .item-info > a + span,
        .item-info > a {{
            white-space: nowrap;
            padding-top:4px;
        }}
        @media (max-width: 425px) {{
            .item-info {{
                flex-wrap: wrap-reverse;
            }}
            .item-keywords {{
                width: 100%;
                margin-bottom: 3px;
            }}
            .item-info > a + span {{
                margin-left: auto !important;
            }}
        }}
        .account-exist {{ 
            color: rgb(22, 144, 119); 
        }} 
        .account-dont-exist {{ 
            color: rgb(236, 94, 94); 
        }}
        .query-content {{
            position: relative;
            overflow-x: clip;
            display: flex;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            text-align: justify;
            color: white;
        }}

        .query {{
            color: white;
            background: #9300FF;
            font-size: 11px;
            border-radius: 3px;
            padding: 0px 4px 1px 4px;
            /*padding: 0px 1px 1px 6px;*/
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            right: 0;
            font-size: 11px;
            background: #9300ff;
            color: #fff;
            padding: 3px 5px;
            border-radius: 6px;
            transition: .15s;
            display: none;
            opacity: 0;
        }}

        .prompt::after {{
            content: "▶";
            position: absolute;
            top: 100%;
            left: 10px;
            color: #9300ff;
            height: 9px;
            transform: rotate(90deg);
        }}

        .query:hover+.prompt {{
            display: block !important;
            opacity: 1 !important;
        }}

        .param-text {{
            overflow: hidden;
            margin-left: 8px;
            font-size: 12px;
        }}

        .empty-list {{
            color: #8a6d3b;
            background: #fce7c4;
            border: 1px solid #fad292;
            display: flex;
            align-items: center;
            height: 35px;
            padding: 0 10px;
            border-radius: 4px;
            margin: 0 auto 15px;
        }}

        .empty-list svg {{
            height: 18px;
            margin-right: 7px;
            fill: #8a6d3b;
        }}

        .pagination svg {{
            height: 100%;
            display: flex;
            align-items: center;
            margin: 0 3px;
            padding: 6px 0 !important;
            width: 22px;
        }}

        .pagination {{
            margin-left: auto;
            display: flex;
            align-items: center;
            /*position: absolute;
                right: 10px;
                bottom: 10px;*/
            font-size: 13px;
            height: 25px;
            user-select: none;
        }}

        .pagination>div>*,
        .pagination>*:not(.pagination > div) {{
            height: 100%;
            padding: 0 7px;
            display: flex !important;
            align-items: center !important;
            cursor: pointer;
            background: white;
        }}

        .h-full {{
            height: 100%;
        }}

        .w-full {{
            width: 100%;
        }}

        .w-half {{
            width: 50%;
        }}

        .pagination>*:first-child {{
            border-radius: 4px 0 0 4px;
        }}

        .pagination>*:last-child {{
            border-radius: 0 4px 4px 0;
        }}

        .pagination>div>* {{
            border-bottom: 1px solid transparent;

        }}

        .pagination>div>*.selected,
        .pagination>div>*:hover {{
            border-bottom: 1px solid #3b5998;
            color: #3b5998;
            font-weight: 600;
        }}

        .pagination>.hovered-angle>svg:hover {{
            background: #3b5998;
            fill: white;
        }}

        .pagination div span {{
            display: flex;
            align-items: center;
        }}

        h2 {{
            font-size: 22px;
        }}

        .object-full_name {{
            font-size: 21px;
            margin-top: 0;
            margin-bottom: 0;
            text-align: center;
            margin-right: 10px;
            margin-bottom: 6px;
        }}

        @media (max-width: 710px) {{
            .tab-head>.tabs:not(.tab-head .pagination) {{
                margin: 0 -5px;
                font-size: 15px;
            }}
        }}

        @media (max-width: 500px) {{
            .item-container {{
                margin-bottom: 12px;
            }}

            .item {{
                padding: 8px 11px;
            }}

            .item-title {{
                font-size: 14px;
            }}

            .item-more {{
                font-size: 13px;
                height: 25px;
            }}

            .item-more svg {{
                width: 11px;
                margin-left: 7px;
            }}

            .item-content {{
                font-size: 11px;
                margin-top: 5px;
                margin-bottom: auto;
                line-height: 17px;
            }}

            .item-param {{
                font-size: 11px;
                line-height: 14px;
            }}
        }}

        .filter-search-arbitrary {{
            padding: 15px 7.5px 0;
            width: 50%;
        }}

        .filter-search-arbitrary .input {{
            position: relative;
            display: flex;
            box-shadow: 0 0 4px #7f7f7f;
            max-width: 450px;
            margin: auto;
        }}

        .filter-search-arbitrary .input>input {{
            width: 100%;
            height: 28px;
            padding-left: 7px;
            border-radius: 4px;
            border: none;
            outline: none;
        }}

        .filter-search-arbitrary .input svg {{
            position: absolute;
            right: 7px;
            top: 0;
            bottom: 0;
            width: 14px;
            display: flex;
            align-items: center;
            height: 100%;
            fill: #706f6f;
            cursor: pointer;
            transition: .15s;
        }}

        .filter-search-arbitrary .input svg:hover {{
            fill: black;
        }}

        .filter-search-arbitrary .input.selected svg {{
            transform: rotateX(180deg);
        }}

        .scrollbar::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .scrollbar::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .scrollbar::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 5px;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 0 4px #7f7f7f;
        }}

        .arbitrary-keys>div:first-child {{
            border-radius: 4px;
            min-height: 50px;
            max-height: 270px;
            overflow-y: scroll;
            overflow-x: hidden;
            background: white;
            padding: 8px 10px;
            font-size: 14px;
            position: relative;
            z-index: 5;
        }}

        .arbitrary-keys:not(.arbitrary-keys.show) {{
            display: none;
        }}

        .arbitrary-key {{
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }}

        .arbitrary-key span {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .arbitrary-key:not(.arbitrary-key:last-child) {{
            margin-bottom: 8px;
        }}

        .arbitrary-key input {{
            margin: 2px 5px 0 0;
            height: 14.5px !important;
            width: 14.5px !important;
            line-height: 1 !important;
            accent-color: #9300FF;
        }}

        .hovered-angle svg {{
            transition: .15s;
        }}

        svg.first-page,
        svg.last-page {{
            margin: 0;
            padding: 5.65px 0 !important;
            width: 22px;
        }}

        .first-page {{
            margin-left: 22px !important;
        }}

        .last-page {{
            margin-right: 22px !important;
        }}

        .hovered-angle {{
            height: 100%;
        }}

        .pagination {{
            border-radius: 4px;
            overflow: hidden;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page,
        .hovered-angle:not(.hovered-angle:hover) svg.last-page {{
            width: 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg:not(svg.last-page) {{
            border-radius: 0 4px 4px 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page+svg {{
            border-radius: 4px 0 0 4px;
        }}

        .hovered-angle:hover svg.first-page,
        .hovered-angle:hover svg.last-page {{
            margin: 0 !important;
        }}

        .pagination-container {{
            padding: 15px 7.5px 0;
            margin: auto;
        }}

        @media (max-width: 670px) {{

            .hovered-angle:hover svg:not(svg.last-page) {{
                border-radius: 0 4px 4px 0 !important;
            }}

            .hovered-angle:hover svg.first-page+svg {{
                border-radius: 4px 0 0 4px !important;
            }}

            .filter-search-arbitrary {{
                width: 100%;
            }}

            .wrap-reverse-container {{
                flex-wrap: wrap-reverse;
            }}

            svg.first-page,
            svg.last-page {{
                display: none !important;
            }}

            .pagination .flex.h-full {{
                max-width: 250px;
                overflow-y: hidden;
                overflow-x: scroll;
                margin-bottom: 0px;
                min-height: 34px !important;
            }}

            .pagination .flex.h-full>* {{
                height: 26px !important;
            }}

            .pagination {{
                height: 33px;
                margin-bottom: -8px;
            }}

            .pagination .hovered-angle {{
                padding-bottom: 8px;
            }}
        }}

        .filter-btns {{
            background: white;
            position: relative;
            z-index: 1;
            border-top: 1px solid #ccc;
            font-size: 15px;
            display: flex;
        }}

        .filter-btns span {{
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-around;
            height: 38px;
            cursor: pointer;
            transition: .15s;
            padding-bottom: 1px;
        }}

        .filter-btns span:first-child {{
            border-right: 1px solid #ccc;
        }}

        .filter-btns span:hover {{
            color: white;
            background: #9300FF;
        }}

        .filter-info {{
            position: absolute !important;
            top: unset !important;
            bottom: 38px !important;
            right: 0 !important;
            margin: 5px;
            z-index: 15;
            width: 18.5px !important;
            height: 18.5px !important;
        }}

        .filter-info svg {{
            width: 18.5px !important;
            height: 18.5px !important;
            fill: rgba(131, 131, 131, 0.58) !important;
            transform: rotateX(0deg) !important;
        }}

        .filter-info svg:hover {{
            fill: #838383 !important;
        }}

        .filter-info .filter-info_prompt {{
            position: absolute;
            bottom: calc(100% + 9px);
            right: 0;
            background: #838383;
            color: white;
            font-size: 11px;
            white-space: nowrap;
            padding: 3px 5px;
            border-radius: 4px;
            transition: .15s;
        }}

        .filter-info_prompt::after {{
            content: "▶";
            position: absolute;
            top: calc(100% - 1.5px);
            right: 8.5px;
            color: #838383;
            height: 3px;
            transform: rotate(90deg);
        }}

        .filter-info svg:not(.filter-info svg:hover)+.filter-info_prompt {{
            opacity: 0;
            pointer-events: none;
        }}

        .similars-range {{
            max-width: 300px;
            width: 100%;
            /*max-height: 25px;*/
            position: relative;

            margin: 15px 7.5px 0;
            padding-top: 11.5px;
            height: 25px;
            background: white;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0, 0, 0, .15);
            margin-left: auto !important;
            margin-right: auto !important;
        }}

        .similars-range input {{
            position: absolute;
            top: 0;
            left: 0;
        }}

        /* Range */

        [slider] {{
            position: relative;
            height: 3px;
            border-radius: 10px;
            text-align: left;
            display: flex;
            align-items: center;
        }}

        [slider]>div {{
            position: absolute;
            left: 13px;
            right: 15px;
            height: 3px;
        }}

        [slider]>div>[inverse-left] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[inverse-right] {{
            position: absolute;
            right: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[range] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 14px;
            background-color: #4169e1;
        }}

        [slider]>div>[thumb] {{
            position: absolute;
            top: -5px;
            z-index: 2;
            height: 12px;
            width: 12px;
            text-align: left;
            margin-left: -7px;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
            background-color: #FFF;
            border-radius: 3px;
            outline: none;
        }}

        [slider]>input[type=range] {{
            position: absolute;
            pointer-events: none;
            -webkit-appearance: none;
            z-index: 3;
            height: 3px;
            top: -2px;
            width: 100%;
            -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
            filter: alpha(opacity=0);
            -moz-opacity: 0;
            -khtml-opacity: 0;
            opacity: 0;
        }}

        div[slider]>input[type=range]::-ms-track {{
            -webkit-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]::-moz-range-track {{
            -moz-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]:focus::-webkit-slider-runnable-track {{
            background: transparent;
            border: transparent;
        }}

        div[slider]>input[type=range]:focus {{
            outline: none;
        }}

        div[slider]>input[type=range]::-ms-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-moz-range-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-webkit-slider-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
            -webkit-appearance: none;
        }}

        div[slider]>input[type=range]::-ms-fill-lower {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-fill-upper {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-tooltip {{
            display: none;
        }}

        [slider]>div>[sign] {{
            font-size: 15px;
            opacity: 0;
            position: absolute;
            margin-left: -13px;
            top: -2.4375em;
            z-index: 3;
            background-color: #4169e1;
            color: #fff;
            width: 1.75em;
            height: 1.75em;
            border-radius: 1.75em;
            -webkit-border-radius: 1.75em;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            text-align: center;
        }}

        [slider]>div>[sign]:after {{
            position: absolute;
            content: '';
            left: 0;
            border-radius: 1em;
            top: calc(1.1875em + 1px);
            border-left: 0.875em solid transparent;
            border-right: 0.875em solid transparent;
            border-top-width: 1em;
            border-top-style: solid;
            border-top-color: #4169e1;
        }}

        [slider]>div>[sign]>span {{
            font-size: 10px;
            font-weight: 700;
            line-height: 28px;
        }}

        [slider]:hover>div>[sign] {{
            opacity: 1;
        }}

        .clone {{
            width: 16px;
            height: 16px;
            fill: #4169e1;
        }}
        .seen_link {{
            opacity: 0.8;
        }}

        .seen_link .item {{
            box-shadow: none;
            background: #c4d9ce;
        }}
        .leaks {{
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            padding: 6px 6px 10px 6px;
            gap: 5px;
            background: #cdcdcd;
            margin: 0 3%;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,.25);
            width: 100%;
        }}
        .leaks .flex {{
            gap: 6px 35px;
            padding: 0 5px;
        }}
        .leak-description {{
            padding: 6px 12px 7px 10px;
            font-size: 18px;
            background: white;
            border-radius: 4px 4px 0 0;
            margin: -6px;
            margin-bottom: 10px;
        }}
        .f-w-600 {{
            font-weight: 600;
        }}
        .leak {{
            white-space: nowrap;
            height: 30px;
            display: flex;
            align-items: center;
            padding: 0 12px 0 10px;
            line-height: 1;
            background: white;
            border-radius: 5px;
        }}
        
        /* .leak:not(.leak:last-child) {{
            border-bottom: 1px solid;
        }}
        .leaks .flex .flex-col:not(.leak:last-child) {{
            border-right: 1px solid;
        }} */
        
        table {{
            background: #0000008c;
        }}
        .gray-color {{
            color: #ccc;
        }}
        .m-b-5 {{
            margin-bottom: 5px;
        }}

/* ------------------------------------ */

.checkmark__circle {{
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 5;
    stroke-miterlimit: 10;
    stroke: #4400ed;
    fill: none;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}}

.checkmark {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: block;
    stroke-width: 6.5;
    stroke: #fff;
    stroke-miterlimit: 10;
    box-shadow: inset 0px 0px 0px #4400ed;
    animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;

    margin-right: 5px;
    position: absolute;
    top: -5px;
    left: -5px;
}}

.checkmark.unseen {{
    top: 6px;
    left: 6px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
}}

.checkmark.unseen.seen_scale {{
    animation: fill .4s ease-in-out .4s forwards, seen_scale .3s ease-in-out .9s both;
}}

.checkmark__check {{
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}}

@keyframes stroke {{
    100% {{
        stroke-dashoffset: 0;
    }}
}}

@keyframes scale {{

    0%,
    100% {{
        transform: none;
    }}

    50% {{
        transform: scale3d(1.1, 1.1, 1);
    }}
}}

@keyframes seen_scale {{
    20% {{
        transform: scale3d(1.1, 1.1, 1);
    }}

    99% {{
        transform: scale3d(0, 0, 0);
    }}

    99% {{
        display: none;
    }}
}}

@keyframes fill {{
    100% {{
        box-shadow: inset 0px 0px 0px 20px #4400ed;
    }}
}}
table tbody tr td:last-child {{ 
    /* font-size: 15px; */ 
}} 
td {{ 
    vertical-align: top; 
}} 
td:first-child, th:first-child {{ 
    border-right: 1px solid #ccc; 
}} 
tr:last-child td {{ 
    border-bottom: none; 
}} 
table table tr td:first-child {{ 
    /* border-right: none; */ 
    border-right-color: #f3f3f3bb; 
}} 
table table tr td {{ 
    border-bottom-color: #f3f3f3bb; 
}} 
td, th {{ 
    background: white; 
    padding: 8px 14px 7px 14px; 
    /* margin-bottom: 5px !important; */ 
    border-bottom: 1px solid #ccc; 
    height: 40px; 
}} 
.td-key {{ 
    letter-spacing: 1px; 
    font-weight: 600; 
    margin-right: 15px; 
}} 
.td-link {{ 
    block-size: border-box; 
    display: inline-block; 
    white-space: nowrap; 
    overflow: hidden; 
    text-overflow: ellipsis; 
    max-width: 400px; 
}} 
.empty-result {{ 
    color: #9d9d9d; 
}}
table table td img {{ 
    padding: 0 5px 5px 0; 
}}
.tag-repeated-count {{ 
    margin-left: auto; 
    margin-right: -5px; 
    background: #9300FF; 
    color: white; 
    padding: 1.5px 3px 2px 4px; 
    border-radius: 4px; 
    font-size: 13px; 
    white-space: nowrap; 
}}
tr > td:first-child {{ 
    text-wrap: balance; 
}}
    </style>"""




TG_STYLE = f"""<style>
        @import url('https://fonts.cdnfonts.com/css/roboto');

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, "Helvetica Neue", Helvetica, sans-serif;
            margin: 0;
            padding: 0;
            background: #e7e7e7;
            overflow-x: hidden;
        }}

        .flex {{
            display: flex;
        }}
        .flex-col {{
            flex-direction: column;
        }}

        .flex-wrap {{
            flex-wrap: wrap;
        }}

        .items-center {{
            align-items: center;
        }}

        .tab-head {{
            position: relative;
            background: white;
            padding: 12px 12px 0px 18px;
            box-shadow: 0 2.5px 4px rgb(184, 183, 183);
            font-size: 16px;

            padding: 7px 20px 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        @media (max-width: 640px) {{
            .tab-head {{
                padding: 7px 8px 0;
                align-items: center;
            }}

            .tab-head .tabs {{
                justify-content: center;
            }}
        }}

        .tab-head .flex div {{
            font-size: 1em !important;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination) {{
            position: relative;
            padding: .625em .5em;
            margin-right: .8125em;
            cursor: pointer;
            background: white;
            user-select: none;
            color: #747474;
            transition: color .15s;
            /*margin-top: .5em;*/
            margin-top: 4px;
            border-bottom: 2px solid transparent;
        }}

        .tab-head .flex>div:not(.tab-head .flex > .pagination):hover,
        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed;
        }}

        .tab-head .flex>.selected {{
            border-bottom: 2px solid #4400ed !important;
            color: #4400ed !important;
        }}

        .tab-count {{
            position: absolute;
            top: -2px;
            right: -4px;
            display: flex;
            align-items: center;
            padding: 0 3px;
            border-radius: 3px;
            height: 16px;
            font-size: 11px;
            /* 12px */
            background: #4400ed;
            color: white;
        }}

        .content {{
            padding: 15px 7.5px 0;
        }}

        .content>div.selected {{
            display: flex;
            flex-wrap: wrap;
            /*padding: 0 2.5px;*/
        }}

        .content>div:not(.content > .selected) {{
            display: none;
        }}

        .item-container {{
            /*min-width: 375px;*/
            width: 50%;
            padding: 0 7.5px;
            margin-bottom: 15px;
        }}

        @media (max-width: 1025px) {{
            .item-container {{
                width: 100%;
            }}
        }}

        .filter-search-arbitrary {{
            margin-left: 7.5px;
        }}

        @media (max-width: 570px) {{
            .item-container {{
                padding: 0 1.5px;
            }}

            .filter-search-arbitrary {{
                margin-left: 1.5px;
            }}
        }}

        .item {{
            background: white;
            padding: 12px 15px;
            border-radius: 4px;
            box-shadow: 0 0 4px #7f7f7f;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}

        .mt-auto {{
            margin-top: auto;
        }}

        .key-word {{
            background: #e0ec90;
            padding: 0 4px;
            border-radius: 4px;
        }}

        .item-title {{
            font-size: 17px;
            font-weight: 600;


            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;

            text-decoration: none;
            color: #333;
        }}

        .item-title:hover {{
            text-decoration: underline;
        }}

        .item-content {{
            font-size: 13px;
            margin-top: 6px;
            margin-bottom: 0px;

            text-align: justify;
            max-height: 80px;
            line-height: 20px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            margin-bottom: auto;
        }}

        .item-more {{
            margin-left: auto;
            font-size: 14px;
            border: 1px solid #000;

            border: 1px solid #e7eaec;
            font-size: 15px;
            height: 29px;
            padding: 0 8px;
            border-radius: 3px;
            transition: .25s;

            display: flex;
            align-items: center;

            text-decoration: none;
            color: #333;
        }}

        .item-more:hover {{
            background: #e7eaec70;
            text-decoration: underline;
        }}

        .item-more svg {{
            width: 13px;
            margin-left: 7px;
        }}

        .item-param {{
            font-size: 13px;
            display: flex;
            /*white-space: nowrap;*/
            font-weight: 600;
            position: relative;
        }}
        .item-info > a + span,
        .item-info > a {{
            white-space: nowrap;
            padding-top:4px;
        }}
        @media (max-width: 425px) {{
            .item-info {{
                flex-wrap: wrap-reverse;
            }}
            .item-keywords {{
                width: 100%;
                margin-bottom: 3px;
            }}
            .item-info > a + span {{
                margin-left: auto !important;
            }}
        }}
        .account-exist {{ 
            color: rgb(22, 144, 119); 
        }} 
        .account-dont-exist {{ 
            color: rgb(236, 94, 94); 
        }}
        .query-content {{
            position: relative;
            overflow-x: clip;
            display: flex;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            text-align: justify;
            color: white;
        }}

        .query {{
            color: white;
            background: #9300FF;
            font-size: 11px;
            border-radius: 3px;
            padding: 0px 4px 1px 4px;
            /*padding: 0px 1px 1px 6px;*/
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .prompt {{
            position: absolute;
            bottom: calc(100% + 7px);
            right: 0;
            font-size: 11px;
            background: #9300ff;
            color: #fff;
            padding: 3px 5px;
            border-radius: 6px;
            transition: .15s;
            display: none;
            opacity: 0;
        }}

        .prompt::after {{
            content: "▶";
            position: absolute;
            top: 100%;
            left: 10px;
            color: #9300ff;
            height: 9px;
            transform: rotate(90deg);
        }}

        .query:hover+.prompt {{
            display: block !important;
            opacity: 1 !important;
        }}

        .param-text {{
            overflow: hidden;
            margin-left: 8px;
            font-size: 12px;
        }}

        .empty-list {{
            color: #8a6d3b;
            background: #fce7c4;
            border: 1px solid #fad292;
            display: flex;
            align-items: center;
            height: 35px;
            padding: 0 10px;
            border-radius: 4px;
            margin: 0 auto 15px;
        }}

        .empty-list svg {{
            height: 18px;
            margin-right: 7px;
            fill: #8a6d3b;
        }}

        .pagination svg {{
            height: 100%;
            display: flex;
            align-items: center;
            margin: 0 3px;
            padding: 6px 0 !important;
            width: 22px;
        }}

        .pagination {{
            margin-left: auto;
            display: flex;
            align-items: center;
            /*position: absolute;
                right: 10px;
                bottom: 10px;*/
            font-size: 13px;
            height: 25px;
            user-select: none;
        }}

        .pagination>div>*,
        .pagination>*:not(.pagination > div) {{
            height: 100%;
            padding: 0 7px;
            display: flex !important;
            align-items: center !important;
            cursor: pointer;
            background: white;
        }}

        .h-full {{
            height: 100%;
        }}

        .w-full {{
            width: 100%;
        }}

        .w-half {{
            width: 50%;
        }}

        .pagination>*:first-child {{
            border-radius: 4px 0 0 4px;
        }}

        .pagination>*:last-child {{
            border-radius: 0 4px 4px 0;
        }}

        .pagination>div>* {{
            border-bottom: 1px solid transparent;

        }}

        .pagination>div>*.selected,
        .pagination>div>*:hover {{
            border-bottom: 1px solid #3b5998;
            color: #3b5998;
            font-weight: 600;
        }}

        .pagination>.hovered-angle>svg:hover {{
            background: #3b5998;
            fill: white;
        }}

        .pagination div span {{
            display: flex;
            align-items: center;
        }}

        h2 {{
            font-size: 22px;
        }}

        .object-full_name {{
            font-size: 21px;
            margin-top: 0;
            margin-bottom: 0;
            text-align: center;
            margin-right: 10px;
            margin-bottom: 6px;
        }}

        @media (max-width: 710px) {{
            .tab-head>.tabs:not(.tab-head .pagination) {{
                margin: 0 -5px;
                font-size: 15px;
            }}
        }}

        @media (max-width: 500px) {{
            .item-container {{
                margin-bottom: 12px;
            }}

            .item {{
                padding: 8px 11px;
            }}

            .item-title {{
                font-size: 14px;
            }}

            .item-more {{
                font-size: 13px;
                height: 25px;
            }}

            .item-more svg {{
                width: 11px;
                margin-left: 7px;
            }}

            .item-content {{
                font-size: 11px;
                margin-top: 5px;
                margin-bottom: auto;
                line-height: 17px;
            }}

            .item-param {{
                font-size: 11px;
                line-height: 14px;
            }}
        }}

        .filter-search-arbitrary {{
            padding: 15px 7.5px 0;
            width: 50%;
        }}

        .filter-search-arbitrary .input {{
            position: relative;
            display: flex;
            box-shadow: 0 0 4px #7f7f7f;
            max-width: 450px;
            margin: auto;
        }}

        .filter-search-arbitrary .input>input {{
            width: 100%;
            height: 28px;
            padding-left: 7px;
            border-radius: 4px;
            border: none;
            outline: none;
        }}

        .filter-search-arbitrary .input svg {{
            position: absolute;
            right: 7px;
            top: 0;
            bottom: 0;
            width: 14px;
            display: flex;
            align-items: center;
            height: 100%;
            fill: #706f6f;
            cursor: pointer;
            transition: .15s;
        }}

        .filter-search-arbitrary .input svg:hover {{
            fill: black;
        }}

        .filter-search-arbitrary .input.selected svg {{
            transform: rotateX(180deg);
        }}

        .scrollbar::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .scrollbar::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .scrollbar::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar {{
            width: 7px;
            height: 6px;
            margin-left: 2px;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-track {{
            margin-left: 2px;
            background-color: transparent;
        }}

        .arbitrary-keys>div:first-child::-webkit-scrollbar-thumb {{
            /*background-color: #eaeaea;*/
            background-color: rgb(170, 227, 255);
            border-radius: 5px;
        }}

        .arbitrary-keys {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 5px;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 0 4px #7f7f7f;
        }}

        .arbitrary-keys>div:first-child {{
            border-radius: 4px;
            min-height: 50px;
            max-height: 270px;
            overflow-y: scroll;
            overflow-x: hidden;
            background: white;
            padding: 8px 10px;
            font-size: 14px;
            position: relative;
            z-index: 5;
        }}

        .arbitrary-keys:not(.arbitrary-keys.show) {{
            display: none;
        }}

        .arbitrary-key {{
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
        }}

        .arbitrary-key span {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .arbitrary-key:not(.arbitrary-key:last-child) {{
            margin-bottom: 8px;
        }}

        .arbitrary-key input {{
            margin: 2px 5px 0 0;
            height: 14.5px !important;
            width: 14.5px !important;
            line-height: 1 !important;
            accent-color: #9300FF;
        }}

        .hovered-angle svg {{
            transition: .15s;
        }}

        svg.first-page,
        svg.last-page {{
            margin: 0;
            padding: 5.65px 0 !important;
            width: 22px;
        }}

        .first-page {{
            margin-left: 22px !important;
        }}

        .last-page {{
            margin-right: 22px !important;
        }}

        .hovered-angle {{
            height: 100%;
        }}

        .pagination {{
            border-radius: 4px;
            overflow: hidden;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page,
        .hovered-angle:not(.hovered-angle:hover) svg.last-page {{
            width: 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg:not(svg.last-page) {{
            border-radius: 0 4px 4px 0;
        }}

        .hovered-angle:not(.hovered-angle:hover) svg.first-page+svg {{
            border-radius: 4px 0 0 4px;
        }}

        .hovered-angle:hover svg.first-page,
        .hovered-angle:hover svg.last-page {{
            margin: 0 !important;
        }}

        .pagination-container {{
            padding: 15px 7.5px 0;
            margin: auto;
        }}

        @media (max-width: 670px) {{

            .hovered-angle:hover svg:not(svg.last-page) {{
                border-radius: 0 4px 4px 0 !important;
            }}

            .hovered-angle:hover svg.first-page+svg {{
                border-radius: 4px 0 0 4px !important;
            }}

            .filter-search-arbitrary {{
                width: 100%;
            }}

            .wrap-reverse-container {{
                flex-wrap: wrap-reverse;
            }}

            svg.first-page,
            svg.last-page {{
                display: none !important;
            }}

            .pagination .flex.h-full {{
                max-width: 250px;
                overflow-y: hidden;
                overflow-x: scroll;
                margin-bottom: 0px;
                min-height: 34px !important;
            }}

            .pagination .flex.h-full>* {{
                height: 26px !important;
            }}

            .pagination {{
                height: 33px;
                margin-bottom: -8px;
            }}

            .pagination .hovered-angle {{
                padding-bottom: 8px;
            }}
        }}

        .filter-btns {{
            background: white;
            position: relative;
            z-index: 1;
            border-top: 1px solid #ccc;
            font-size: 15px;
            display: flex;
        }}

        .filter-btns span {{
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-around;
            height: 38px;
            cursor: pointer;
            transition: .15s;
            padding-bottom: 1px;
        }}

        .filter-btns span:first-child {{
            border-right: 1px solid #ccc;
        }}

        .filter-btns span:hover {{
            color: white;
            background: #9300FF;
        }}

        .filter-info {{
            position: absolute !important;
            top: unset !important;
            bottom: 38px !important;
            right: 0 !important;
            margin: 5px;
            z-index: 15;
            width: 18.5px !important;
            height: 18.5px !important;
        }}

        .filter-info svg {{
            width: 18.5px !important;
            height: 18.5px !important;
            fill: rgba(131, 131, 131, 0.58) !important;
            transform: rotateX(0deg) !important;
        }}

        .filter-info svg:hover {{
            fill: #838383 !important;
        }}

        .filter-info .filter-info_prompt {{
            position: absolute;
            bottom: calc(100% + 9px);
            right: 0;
            background: #838383;
            color: white;
            font-size: 11px;
            white-space: nowrap;
            padding: 3px 5px;
            border-radius: 4px;
            transition: .15s;
        }}

        .filter-info_prompt::after {{
            content: "▶";
            position: absolute;
            top: calc(100% - 1.5px);
            right: 8.5px;
            color: #838383;
            height: 3px;
            transform: rotate(90deg);
        }}

        .filter-info svg:not(.filter-info svg:hover)+.filter-info_prompt {{
            opacity: 0;
            pointer-events: none;
        }}

        .similars-range {{
            max-width: 300px;
            width: 100%;
            /*max-height: 25px;*/
            position: relative;

            margin: 15px 7.5px 0;
            padding-top: 11.5px;
            height: 25px;
            background: white;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0, 0, 0, .15);
            margin-left: auto !important;
            margin-right: auto !important;
        }}

        .similars-range input {{
            position: absolute;
            top: 0;
            left: 0;
        }}

        /* Range */

        [slider] {{
            position: relative;
            height: 3px;
            border-radius: 10px;
            text-align: left;
            display: flex;
            align-items: center;
        }}

        [slider]>div {{
            position: absolute;
            left: 13px;
            right: 15px;
            height: 3px;
        }}

        [slider]>div>[inverse-left] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[inverse-right] {{
            position: absolute;
            right: 0;
            height: 3px;
            border-radius: 10px;
            background-color: #CCC;
            margin: 0 7px;
        }}

        [slider]>div>[range] {{
            position: absolute;
            left: 0;
            height: 3px;
            border-radius: 14px;
            background-color: #4169e1;
        }}

        [slider]>div>[thumb] {{
            position: absolute;
            top: -5px;
            z-index: 2;
            height: 12px;
            width: 12px;
            text-align: left;
            margin-left: -7px;
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.4);
            background-color: #FFF;
            border-radius: 3px;
            outline: none;
        }}

        [slider]>input[type=range] {{
            position: absolute;
            pointer-events: none;
            -webkit-appearance: none;
            z-index: 3;
            height: 3px;
            top: -2px;
            width: 100%;
            -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";
            filter: alpha(opacity=0);
            -moz-opacity: 0;
            -khtml-opacity: 0;
            opacity: 0;
        }}

        div[slider]>input[type=range]::-ms-track {{
            -webkit-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]::-moz-range-track {{
            -moz-appearance: none;
            background: transparent;
            color: transparent;
        }}

        div[slider]>input[type=range]:focus::-webkit-slider-runnable-track {{
            background: transparent;
            border: transparent;
        }}

        div[slider]>input[type=range]:focus {{
            outline: none;
        }}

        div[slider]>input[type=range]::-ms-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-moz-range-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
        }}

        div[slider]>input[type=range]::-webkit-slider-thumb {{
            pointer-events: all;
            width: 28px;
            height: 28px;
            border-radius: 0px;
            border: 0 none;
            background: red;
            -webkit-appearance: none;
        }}

        div[slider]>input[type=range]::-ms-fill-lower {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-fill-upper {{
            background: transparent;
            border: 0 none;
        }}

        div[slider]>input[type=range]::-ms-tooltip {{
            display: none;
        }}

        [slider]>div>[sign] {{
            font-size: 15px;
            opacity: 0;
            position: absolute;
            margin-left: -13px;
            top: -2.4375em;
            z-index: 3;
            background-color: #4169e1;
            color: #fff;
            width: 1.75em;
            height: 1.75em;
            border-radius: 1.75em;
            -webkit-border-radius: 1.75em;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            text-align: center;
        }}

        [slider]>div>[sign]:after {{
            position: absolute;
            content: '';
            left: 0;
            border-radius: 1em;
            top: calc(1.1875em + 1px);
            border-left: 0.875em solid transparent;
            border-right: 0.875em solid transparent;
            border-top-width: 1em;
            border-top-style: solid;
            border-top-color: #4169e1;
        }}

        [slider]>div>[sign]>span {{
            font-size: 10px;
            font-weight: 700;
            line-height: 28px;
        }}

        [slider]:hover>div>[sign] {{
            opacity: 1;
        }}

        .clone {{
            width: 16px;
            height: 16px;
            fill: #4169e1;
        }}
        .seen_link {{
            opacity: 0.8;
        }}

        .seen_link .item {{
            box-shadow: none;
            background: #c4d9ce;
        }}
        .phones,
        .groups,
        .groups2,
        .leaks {{
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            padding: 6px 6px 10px 6px;
            gap: 5px;
            background: #cdcdcd;
            margin: 0 3%;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,.25);
            width: 100%;
        }}
        .phones .flex,
        .groups .flex,
        .groups2 .flex,
        .leaks .flex {{
            gap: 6px 35px;
            padding: 0 5px;
        }}
        .phones-description,
        .groups-description,
        .groups2-description,
        .leak-description {{
            padding: 6px 12px 7px 10px;
            font-size: 18px;
            background: white;
            border-radius: 4px 4px 0 0;
            margin: -6px;
            margin-bottom: 10px;
        }}
        .f-w-600 {{
            font-weight: 600;
        }}
        .leak {{
            white-space: nowrap;
            height: 30px;
            display: flex;
            align-items: center;
            padding: 0 12px 0 10px;
            line-height: 1;
            background: white;
            border-radius: 5px;
        }}
        /* .leak:not(.leak:last-child) {{
            border-bottom: 1px solid;
        }}
        .leaks .flex .flex-col:not(.leak:last-child) {{
            border-right: 1px solid;
        }} */
        table {{
            background: #0000008c;
        }}
        .gray-color {{
            color: #ccc;
        }}
        .m-b-5 {{
            margin-bottom: 5px;
        }}

/* ------------------------------------ */

.checkmark__circle {{
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 5;
    stroke-miterlimit: 10;
    stroke: #4400ed;
    fill: none;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}}

.checkmark {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: block;
    stroke-width: 6.5;
    stroke: #fff;
    stroke-miterlimit: 10;
    box-shadow: inset 0px 0px 0px #4400ed;
    animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;

    margin-right: 5px;
    position: absolute;
    top: -5px;
    left: -5px;
}}

.checkmark.unseen {{
    top: 6px;
    left: 6px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
}}

.checkmark.unseen.seen_scale {{
    animation: fill .4s ease-in-out .4s forwards, seen_scale .3s ease-in-out .9s both;
}}

.checkmark__check {{
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}}

@keyframes stroke {{
    100% {{
        stroke-dashoffset: 0;
    }}
}}

@keyframes scale {{

    0%,
    100% {{
        transform: none;
    }}

    50% {{
        transform: scale3d(1.1, 1.1, 1);
    }}
}}

@keyframes seen_scale {{
    20% {{
        transform: scale3d(1.1, 1.1, 1);
    }}

    99% {{
        transform: scale3d(0, 0, 0);
    }}

    99% {{
        display: none;
    }}
}}

@keyframes fill {{
    100% {{
        box-shadow: inset 0px 0px 0px 20px #4400ed;
    }}
}}
table tbody tr td:last-child {{ 
    /* font-size: 15px; */ 
}} 
td {{ 
    vertical-align: top; 
}} 
td:first-child, th:first-child {{ 
    border-right: 1px solid #ccc; 
}} 
tr:last-child td {{ 
    border-bottom: none; 
}} 
table table tr td:first-child {{ 
    /* border-right: none; */ 
    border-right-color: #f3f3f3bb; 
}} 
table table tr td {{ 
    border-bottom-color: #f3f3f3bb; 
}} 
td, th {{ 
    background: white; 
    padding: 8px 14px 7px 14px; 
    /* margin-bottom: 5px !important; */ 
    border-bottom: 1px solid #ccc; 
    height: 40px; 
}} 
.td-key {{ 
    letter-spacing: 1px; 
    font-weight: 600; 
    margin-right: 15px; 
}} 
.td-link {{ 
    block-size: border-box; 
    display: inline-block; 
    white-space: nowrap; 
    overflow: hidden; 
    text-overflow: ellipsis; 
    max-width: 400px; 
}} 
.empty-result {{ 
    color: #9d9d9d; 
}}
table table td img {{ 
    padding: 0 5px 5px 0; 
}}
</style>"""
