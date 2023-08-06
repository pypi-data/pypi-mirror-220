import reflex as rx

#https://www.npmjs.com/package/react-colorful
class ColorPicker(rx.Component):
    library = "react-colorful" #from 뒤 npm 패키지 이름
    tag = "HexColorPicker" #import 뒤 리액트 컴포넌트의 태그 이름
    
    #리액트 속성
    color: rx.Var[str]

    #리액트 이벤트
    @classmethod
    def get_controlled_triggers(cls):
        return {
            "on_change": rx.EVENT_ARG
        }

color_picker = ColorPicker.create
