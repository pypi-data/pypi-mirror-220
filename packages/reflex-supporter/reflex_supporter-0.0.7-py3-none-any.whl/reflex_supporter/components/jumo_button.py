import reflex as rx

#https://www.npmjs.com/package/react-supporter
class JumoButton(rx.Component):
    library = "react-supporter" #from 뒤 npm 패키지 이름
    tag = "JumoButton" #import 뒤 리액트 컴포넌트의 태그 이름
    
    #리액트 속성
    background_color: rx.Var[str]
    font_color: rx.Var[str]

    #리액트 이벤트
    @classmethod
    def get_controlled_triggers(cls):
        return {
            "on_click": rx.EVENT_ARG
        } 

jumo_button = JumoButton.create
