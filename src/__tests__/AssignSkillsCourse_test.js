import { render, screen, waitFor, fireEvent} from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import AssignSkillsCourse from '../pages/AssignSkillsCourse';
import '@testing-library/jest-dom'
import axios from 'axios'

jest.mock('axios')

test('Check if all skills checkbox are showns', async() => {
    axios.get
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: [
                    {
                        "Skill_Desc": "Analysis on how a brand is currently perceived in the market, proceeds to planning how the brand should be perceived",
                        "Skill_ID": "BM01",
                        "Skill_Name": "Brand Management",
                        "Skill_Status": null
                    },
                    {
                        "Skill_Desc": "For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.",
                        "Skill_ID": "CM01",
                        "Skill_Name": "Change Management",
                        "Skill_Status": null
                    },
                ]
            }
        })
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: ['BM01'],
                name: 'Systems Thinking and Design'
            }
        })       

    await act(async() => {
        render(<AssignSkillsCourse/>)
    })

    await waitFor(() => {
        const skill_list = screen.getByTestId('skill_list').children
        expect(skill_list).toHaveLength(2)
    })
});

test('Check if the assigned skills are checked', async() => {
    axios.get
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: [
                    {
                        "Skill_Desc": "Analysis on how a brand is currently perceived in the market, proceeds to planning how the brand should be perceived",
                        "Skill_ID": "BM01",
                        "Skill_Name": "Brand Management",
                        "Skill_Status": null
                    },
                    {
                        "Skill_Desc": "For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.",
                        "Skill_ID": "CM01",
                        "Skill_Name": "Change Management",
                        "Skill_Status": null
                    },
                ]
            }
        })
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: ['BM01'],
                name: 'Systems Thinking and Design'
            }
        })       

    await act(async() => {
        render(<AssignSkillsCourse/>)
    })

    await waitFor(() => {
        const checkboxEl = screen.getByLabelText('Brand Management')
        expect(checkboxEl).toBeChecked()
    })
});

test('Check if error message is shown when no skill checkbox is being checked', async() => {
    axios.get
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: [
                    {
                        "Skill_Desc": "Analysis on how a brand is currently perceived in the market, proceeds to planning how the brand should be perceived",
                        "Skill_ID": "BM01",
                        "Skill_Name": "Brand Management",
                        "Skill_Status": null
                    },
                    {
                        "Skill_Desc": "For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.",
                        "Skill_ID": "CM01",
                        "Skill_Name": "Change Management",
                        "Skill_Status": null
                    },
                ]
            }
        })
        .mockResolvedValueOnce({
            data: {
                code: 200,
                data: ['BM01'],
                name: 'Systems Thinking and Design'
            }
        })       

    await act(async() => {
        render(<AssignSkillsCourse/>)
    })

    fireEvent.click(screen.getByLabelText("Brand Management"))
    fireEvent.click(screen.getByRole("button"))

    await waitFor(() => {
        const checkboxEl = screen.getByTestId('ErrorOutlineIcon')
        expect(checkboxEl).toBeInTheDocument()
    })
});

